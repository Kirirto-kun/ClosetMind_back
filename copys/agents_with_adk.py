import asyncio
import json
from typing import AsyncGenerator, List, Dict, Any
from google.adk.agents import LlmAgent, SequentialAgent, BaseAgent
from google.adk.tools import FunctionTool, ToolContext
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from src.utils.google_search import google_search, google_lens_search
from src.utils.scrap_website import scrap_website
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models.clothing import ClothingItem
from src.models.user import User
from src.utils.auth import get_current_user


# Function tools for the search agent
async def search_web(query: str) -> str:
    """
    Searches the web using Google Search API and returns results with links.
    
    Args:
        query: Search query string
        
    Returns:
        JSON string containing search results with links
    """
    try:
        result = await google_search(query)
        data = json.loads(result)
        
        # Extract links from search results
        links = []
        if 'organic' in data:
            for item in data['organic']:
                if 'link' in item:
                    links.append({
                        'title': item.get('title', ''),
                        'link': item['link'],
                        'snippet': item.get('snippet', '')
                    })
        
        return json.dumps({'status': 'success', 'links': links, 'query': query})
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})


async def search_by_image(image_url: str) -> str:
    """
    Searches using Google Lens API with an image URL.
    
    Args:
        image_url: URL of the image to search
        
    Returns:
        JSON string containing search results with links
    """
    try:
        result = await google_lens_search(image_url)
        data = json.loads(result)
        
        # Extract links from lens search results
        links = []
        if 'visual_matches' in data:
            for item in data['visual_matches']:
                if 'link' in item:
                    links.append({
                        'title': item.get('title', ''),
                        'link': item['link'],
                        'snippet': item.get('snippet', '')
                    })
        
        return json.dumps({'status': 'success', 'links': links, 'image_url': image_url})
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})


async def scrape_websites(links_json: str) -> str:
    """
    Scrapes multiple websites and returns their markdown content.
    
    Args:
        links_json: JSON string containing list of links to scrape
        
    Returns:
        JSON string containing scraped content for each URL
    """
    try:
        links_data = json.loads(links_json)
        if 'links' not in links_data:
            return json.dumps({'status': 'error', 'message': 'Invalid links format'})
        
        scraped_content = []
        for link_info in links_data['links'][:5]:  # Limit to 5 links to avoid timeouts
            try:
                url = link_info['link']
                result = await scrap_website(url)
                if result and hasattr(result, 'markdown'):
                    scraped_content.append({
                        'url': url,
                        'title': link_info.get('title', ''),
                        'content': result.markdown[:5000],  # Limit content size
                        'status': 'success'
                    })
                else:
                    scraped_content.append({
                        'url': url,
                        'title': link_info.get('title', ''),
                        'content': '',
                        'status': 'failed',
                        'error': 'No markdown content returned'
                    })
            except Exception as e:
                scraped_content.append({
                    'url': link_info['link'],
                    'title': link_info.get('title', ''),
                    'content': '',
                    'status': 'failed',
                    'error': str(e)
                })
        
        return json.dumps({'status': 'success', 'scraped_data': scraped_content})
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})


async def extract_key_info(scraped_data_json: str) -> str:
    """
    Extracts key information (name, price, link) from scraped content using LLM.
    
    Args:
        scraped_data_json: JSON string containing scraped website data
        
    Returns:
        JSON string containing extracted key information
    """
    try:
        scraped_data = json.loads(scraped_data_json)
        if 'scraped_data' not in scraped_data:
            return json.dumps({'status': 'error', 'message': 'Invalid scraped data format'})
        
        extracted_items = []

        # Lazy import of generative model to avoid heavy import at module load
        from google.genai import GenerativeModel

        model = GenerativeModel("gemini-2.5-pro-preview-06-05")

        for item in scraped_data['scraped_data']:
            if item['status'] != 'success' or not item['content']:
                continue

            markdown_snippet = item['content']

            prompt = (
                """You are extracting structured e-commerce data from raw markdown of a product web page.\n"
                "Return ONLY valid minified JSON with exactly these keys: \n"
                "  name (string) – product/service name,\n"
                "  price (string) – price with currency symbol if present, or \"Price not found\" if absent,\n"
                "  description (string) – concise 1-2 sentence description (max 120 chars).\n"
                "Do NOT wrap the JSON in markdown fences or add extra text.\n\n"
                f"Markdown:\n{markdown_snippet}"""
            )

            try:
                gen_resp = await model.generate_content_async(prompt)
                print(gen_resp.text)
                # The model sometimes adds markdown fences or text – try to locate JSON substring
                raw_out = gen_resp.text.strip()
                json_start = raw_out.find('{')
                json_end = raw_out.rfind('}') + 1
                structured = json.loads(raw_out[json_start:json_end])
            except Exception:
                # Fallback to naive extraction using title
                structured = {
                    "name": item.get("title", "N/A"),
                    "price": "Price not found",
                    "description": markdown_snippet[:120],
                }

            extracted_items.append({
                "link": item["url"],
                **structured,
            })
        
        return json.dumps({'status': 'success', 'extracted_items': extracted_items})
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})


# Create function tools
search_web_tool = FunctionTool(func=search_web)
search_image_tool = FunctionTool(func=search_by_image)
scrape_websites_tool = FunctionTool(func=scrape_websites)
extract_info_tool = FunctionTool(func=extract_key_info)


# Step 1: Search Agent - Finds data on the internet
search_agent = LlmAgent(
    name="SearchAgent",
    model="gemini-2.5-pro-preview-06-05",
    description="Agent that searches the internet using Google Search or Google Lens",
    instruction="""You are a search specialist. When given a search query, use the search_web tool to find relevant links. 
    If given an image URL, use the search_by_image tool instead. Return the results in JSON format with all found links.""",
    tools=[search_web_tool, search_image_tool],
    output_key="search_results"
)

# Step 2: Scraping Agent - Scrapes websites from found links
scraping_agent = LlmAgent(
    name="ScrapingAgent", 
    model="gemini-2.5-pro-preview-06-05",
    description="Agent that scrapes websites and converts them to markdown",
    instruction="""You are a web scraping specialist. Take the search results from the previous step and use the scrape_websites tool 
    to get the markdown content of each website. Focus on the most relevant links.""",
    tools=[scrape_websites_tool],
    output_key="scraped_content"
)

# Step 3: Extraction Agent - Extracts key information using LLM
extraction_agent = LlmAgent(
    name="ExtractionAgent",
    model="gemini-2.5-pro-preview-06-05", 
    description="Agent that extracts key information from scraped content",
    instruction="""You are a data extraction specialist. Take the scraped content and use the extract_info_tool to find:
    - Product/item names
    - Prices (if available)
    - Direct links
    - Brief descriptions
    Return structured data that's easy to understand.""",
    tools=[extract_info_tool],
    output_key="extracted_data"
)

# Step 4: Response Agent - Formats the final response
response_agent = LlmAgent(
    name="ResponseAgent",
    model="gemini-2.5-pro-preview-06-05",
    description="Agent that formats the final response for the user",
    instruction="""You are a response formatter. Take all the extracted data and create a well-formatted, 
    user-friendly response that includes:
    - A summary of what was found
    - Detailed information about each item (name, price, link, description)
    - Clear formatting that's easy to read
    Make the response comprehensive but organized.""",
    output_key="final_response"
)

# Multi-step Search and Processing Agent (Sequential workflow)
search_processing_agent = SequentialAgent(
    name="SearchProcessingAgent",
    description="Multi-step agent that searches, scrapes, extracts, and formats information from the web",
    sub_agents=[search_agent, scraping_agent, extraction_agent, response_agent]
)

# Simple General Query Agent
general_query_agent = LlmAgent(
    name="GeneralQueryAgent",
    model="gemini-2.5-pro-preview-06-05",
    description="Agent that handles general questions and conversations",
    instruction="""You are a helpful assistant that answers general questions and engages in conversation. 
    Provide accurate, helpful, and friendly responses to user queries. If the user asks about searching for products 
    or specific information online, suggest they specify they want to search the web.""",
    output_key="general_response"
)

async def get_user_wardrobe(tool_context: ToolContext) -> str:
    """
    Retrieves all clothing items from the authenticated user's wardrobe.
    The user is identified from the session context.
    """
    try:
        user_id = tool_context.session.state.get("user_id")
        if not user_id:
            return json.dumps({'status': 'error', 'message': 'User not authenticated or user_id not in session state.'})

        db = SessionLocal()
        items = db.query(ClothingItem).filter(ClothingItem.user_id == user_id).all()
        
        wardrobe = []
        for item in items:
            wardrobe.append({
                'id': item.id,
                'name': item.name,
                'image_url': item.image_url,
                'category': item.category,
                'features': item.features
            })
        
        return json.dumps({'status': 'success', 'wardrobe': wardrobe})
    except Exception as e:
        return json.dumps({'status': 'error', 'message': str(e)})
    finally:
        db.close()

# Create function tool for wardrobe access
get_wardrobe_tool = FunctionTool(func=get_user_wardrobe)

# Outfit Recommendation Agent
outfit_agent = LlmAgent(
    name="OutfitRecommendationAgent",
    model="gemini-2.5-pro-preview-06-05",
    description="Agent that creates outfit recommendations from user's wardrobe",
    instruction="""You are a fashion expert that creates outfit recommendations. When a user asks for an outfit:
    1. Access the user's wardrobe using the `get_wardrobe_tool` to see their clothing items.
    2. Based on the user's request and available items, create one or more outfit combinations.
    3. Return a well-formatted response with:
       - A description of the outfit.
       - Links to each clothing item's image.
       - A brief explanation of why these items work together.
    If the wardrobe is empty or no suitable outfits can be made, inform the user.""",
    tools=[get_wardrobe_tool],
    output_key="outfit_recommendation"
)

# Coordinator Agent (Root Agent)
coordinator_agent = LlmAgent(
    name="CoordinatorAgent",
    model="gemini-2.5-pro-preview-06-05",
    description="Main coordinator that routes requests to appropriate sub-agents",
    instruction="""You are the main coordinator. Analyze user requests and decide which agent to use:

    1. If the user wants to search for products, information, or anything that requires web search and data extraction, 
       transfer to SearchProcessingAgent using: "I need to search the web and process the results for you. Let me transfer this to the SearchProcessingAgent."

    2. If the user has general questions, wants to chat, or needs basic information that doesn't require web search,
       transfer to GeneralQueryAgent using: "I'll help you with that general question. Let me transfer this to the GeneralQueryAgent."

    3. If the user wants outfit recommendations or asks about creating outfits from their wardrobe, or just wants to ask something about their wardrobe,
       transfer to OutfitRecommendationAgent using: "I'll help you create an outfit from your wardrobe. Let me transfer this to the OutfitRecommendationAgent."

    Always transfer to the appropriate sub-agent based on the request type. Do not try to handle requests yourself.""",
    sub_agents=[search_processing_agent, general_query_agent, outfit_agent]
)

# Root agent for the API
root_agent = coordinator_agent


async def process_user_request(message: str, user_id: int) -> str:
    """
    Process user request through the multi-agent system.
    
    Args:
        message: User's message/request
        user_id: The ID of the authenticated user.
        
    Returns:
        Response from the appropriate agent
    """
    try:
        # Instead of manually creating an InvocationContext (which requires many
        # internal services), we'll leverage the ADK `Runner` which handles all
        # low-level details for us (session service, invocation IDs, context
        # creation, etc.).

        from google.adk.sessions import InMemorySessionService, Session
        from google.adk.runners import Runner
        from google.genai import types

        # Simple in-memory session service for this example.
        session_service = InMemorySessionService()

        # Ensure a session exists and has the user_id in its state
        try:
            session = await session_service.get_session(
                app_name="ClosetMind",
                user_id="user_closetmind",
                session_id="session_closetmind",
            )
            session.state["user_id"] = user_id
            await session_service.update_session(session)
        except Exception:
            # Session does not exist, create it.
            await session_service.create_session(
                app_name="ClosetMind",
                user_id="user_closetmind",
                session_id="session_closetmind",
                state={"user_id": user_id},
            )

        # Initialize the runner with our root agent and session service.
        runner = Runner(agent=root_agent, session_service=session_service, app_name="ClosetMind")

        # Wrap the raw user text in a `Content` object expected by the runner.
        user_content = types.Content(role="user", parts=[types.Part(text=message)])

        final_answer: str | None = None

        # Stream events; keep updating `final_answer` when we hit a final response.
        async for event in runner.run_async(
            user_id="user_closetmind",
            session_id="session_closetmind",
            new_message=user_content,
        ):
            if not (event.content and getattr(event.content, "parts", None)):
                continue

            # Extract first textual part (many events include only one part)
            text_part = event.content.parts[0]
            if not (hasattr(text_part, "text") and text_part.text):
                continue

            # If the event signals it is the final response from the agent tree, store it
            if hasattr(event, "is_final_response") and callable(event.is_final_response):
                if event.is_final_response():
                    final_answer = text_part.text
            else:
                # Fallback: if no explicit flag, just keep updating; the last message will be our answer
                final_answer = text_part.text

        if final_answer:
            return final_answer

        # Fallback if no content was returned at all
        return "I apologize, but I couldn't process your request at this time."
        
    except Exception as e:
        return f"An error occurred while processing your request: {str(e)}"