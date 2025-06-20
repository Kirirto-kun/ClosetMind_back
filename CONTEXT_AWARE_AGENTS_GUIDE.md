# Context-Aware Agents System

## 🎯 Обзор

Система агентов была улучшена для **полной поддержки контекста диалога**. Теперь все агенты понимают историю разговора, помнят предпочтения пользователя и могут обрабатывать уточнения и отзывы.

## 🧠 Ключевые улучшения

### 1. **История чата для всех агентов**
- ✅ **Search Agent** - помнит предыдущие поиски и предпочтения
- ✅ **Outfit Agent** - учитывает стиль и отзывы пользователя  
- ✅ **General Agent** - поддерживает контекст разговора
- ✅ **Coordinator Agent** - понимает общий контекст и направляет правильные промпты

### 2. **Контекстуальные промпты**
- 🎯 **Анализ истории** - извлечение релевантной информации
- 🎯 **Создание контекста** - формирование улучшенных промптов
- 🎯 **Передача контекста** - отправка полной картины агентам

### 3. **Обучение на предпочтениях**
- 📚 **Search**: бюджет, бренды, стиль продуктов
- 📚 **Outfit**: цвета, стили, комфорт, случаи
- 📚 **General**: интересы и темы разговоров

## 🔄 Как работает контекст

### Coordinator Agent - Мозг системы

```python
def create_contextual_prompt(user_message: str, chat_history: MessageHistory, agent_type: str) -> str:
    # Анализирует последние 6 сообщений
    # Извлекает релевантную информацию по типу агента
    # Создает улучшенный промпт с контекстом
```

**Пример контекстуального промпта:**
```
Based on our conversation context:
Previous: Найди мне черную футболку до $30
Previous: Что-то подешевле и другого бренда

Current request: Покажи еще варианты

Please consider the conversation history when providing your response...
```

### Search Agent - Умный поиск

**Контекстуальные возможности:**
- 🔍 **Помнит бюджет** - "что-то дешевле" → ищет в указанном диапазоне
- 🔍 **Учитывает отзывы** - "другой бренд" → исключает предыдущие бренды  
- 🔍 **Понимает стиль** - "более формальное" → корректирует поиск
- 🔍 **Отслеживает предпочтения** - помнит любимые категории

**Примеры диалогов:**
```
Пользователь: Найди черную футболку
Агент: [показывает результаты]

Пользователь: Что-то подешевле 
Агент: [ищет более дешевые варианты, помня о предыдущем поиске]

Пользователь: И другого бренда
Агент: [исключает предыдущие бренды, сохраняет ценовой диапазон]
```

### Outfit Agent - Личный стилист

**Контекстуальные возможности:**
- 👗 **Изучает стиль** - отслеживает предпочтения пользователя
- 👗 **Помнит отзывы** - "слишком формально" → более casual варианты
- 👗 **Учитывает комфорт** - "неудобно" → приоритет комфорту
- 👗 **Адаптируется к случаям** - помнит потребности для разных событий

**Примеры диалогов:**
```
Пользователь: Что надеть на работу?
Агент: [предлагает business-casual наряд]

Пользователь: Слишком формально для нашего офиса
Агент: [предлагает более casual, но все еще подходящий для работы]

Пользователь: А что насчет цвета? Предпочитаю синий
Агент: [запоминает предпочтение и предлагает синие варианты]
```

## 📋 Архитектура системы

### 1. Coordinator Agent
```python
async def coordinate_request(message: str, user_id: int, db: Session, chat_id: int):
    # 1. Получает историю чата
    history = await get_chat_history(db, chat_id)
    
    # 2. Передает контекст агенту-координатору
    result = await coordinator_agent.run(
        message,
        deps=deps,
        message_history=history.to_pydantic_ai_messages()
    )
```

### 2. Специализированные агенты
```python
async def search_products(ctx: RunContext[CoordinatorDependencies], user_message: str):
    # 1. Получает историю чата
    history = await get_chat_history(ctx.deps.db, ctx.deps.chat_id)
    
    # 2. Создает контекстуальный промпт
    contextual_prompt = create_contextual_prompt(user_message, history, "search")
    
    # 3. Запускает агента с контекстом
    result = await search_agent.run(
        contextual_prompt,
        message_history=history.to_pydantic_ai_messages()
    )
```

## 🎯 Практические сценарии

### Сценарий 1: Поиск товаров с уточнениями
```
1. "Найди мне кроссовки Nike"
   → Агент ищет кроссовки Nike

2. "Что-то подешевле"  
   → Агент помнит про Nike, ищет более дешевые варианты

3. "Может другой бренд?"
   → Агент ищет кроссовки других брендов в том же ценовом диапазоне

4. "Для бега"
   → Агент фокусируется на беговых кроссовках с учетом бюджета
```

### Сценарий 2: Подбор наряда с корректировками
```
1. "Что надеть на свидание?"
   → Агент предлагает романтичный наряд

2. "Слишком нарядно, что-то попроще"
   → Агент предлагает casual-chic вариант

3. "Мне не нравится этот цвет"
   → Агент меняет цветовую гамму, сохраняя стиль

4. "А если погода прохладная?"
   → Агент добавляет верхнюю одежду, помня стиль и предпочтения
```

### Сценарий 3: Смешанный диалог
```
1. "Найди черное платье" (Search Agent)
   → Поиск черных платьев

2. "Как его лучше сочетать?" (Outfit Agent)  
   → Агент помнит про черное платье и предлагает аксессуары

3. "А какая обувь подойдет?" (Outfit Agent)
   → Продолжает работу с тем же платьем

4. "Покажи похожие платья других цветов" (Search Agent)
   → Возвращается к поиску, помня параметры исходного платья
```

## 🚀 Технические детали

### Message History Format
```python
class MessageHistory(BaseModel):
    messages: List[dict] = Field(default_factory=list)
    
    def to_pydantic_ai_messages(self) -> List[ModelMessage]:
        # Конвертация в формат PydanticAI
```

### Contextual Prompt Creation
```python
def create_contextual_prompt(user_message: str, chat_history: MessageHistory, agent_type: str) -> str:
    # Анализ последних 6 сообщений
    recent_messages = chat_history.messages[-6:]
    
    # Извлечение релевантного контекста
    if agent_type == "search":
        # Поиск упоминаний продуктов, цен, брендов
    elif agent_type == "outfit":  
        # Поиск упоминаний одежды, стиля, случаев
        
    # Формирование улучшенного промпта
    return enhanced_prompt
```

### Enhanced System Prompts
Каждый агент теперь включает:
```
CONVERSATION CONTEXT AWARENESS:
- Access to conversation history
- Learning from user feedback  
- Preference tracking over time
- Contextual refinement capabilities

CONTEXTUAL EXAMPLES:
- "something cheaper" → focus on lower prices
- "different style" → adjust style parameters
- "more comfortable" → prioritize comfort
```

## 📊 Результаты улучшений

### До контекстуальных агентов
- ❌ Каждый запрос обрабатывался изолированно
- ❌ Агенты не помнили предпочтения  
- ❌ Пользователю приходилось повторять контекст
- ❌ Неэффективная обработка уточнений

### После контекстуальных агентов  
- ✅ **Полная память** разговора
- ✅ **Изучение предпочтений** пользователя
- ✅ **Умные уточнения** без потери контекста
- ✅ **Персонализированные** рекомендации
- ✅ **Естественный диалог** как с человеком

## 🎉 Преимущества

1. **Естественный диалог** - как разговор с человеком-консультантом
2. **Память предпочтений** - не нужно повторять требования  
3. **Умные уточнения** - "что-то подешевле" понимается в контексте
4. **Персонализация** - рекомендации улучшаются со временем
5. **Эффективность** - меньше повторений, больше точности

## 🛠️ Для разработчиков

### Добавление нового контекстуального агента
```python
# 1. Добавьте поддержку message_history в агент
async def my_agent_function(query: str, message_history: List[ModelMessage] = None):
    agent = get_my_agent()
    result = await agent.run(query, message_history=message_history)
    return result.data

# 2. Обновите system prompt с CONVERSATION CONTEXT AWARENESS
system_prompt = """
CONVERSATION CONTEXT AWARENESS:
- Analyze conversation history for relevant context
- Learn user preferences from previous interactions
- Handle follow-up questions and refinements
"""

# 3. Добавьте в coordinator_agent.py
async def my_tool(ctx: RunContext[CoordinatorDependencies], user_message: str):
    history = await get_chat_history(ctx.deps.db, ctx.deps.chat_id)
    contextual_prompt = create_contextual_prompt(user_message, history, "my_type")
    return await my_agent_function(contextual_prompt, history.to_pydantic_ai_messages())
```

Система теперь **полностью контекстуальна** и обеспечивает естественный диалог с сохранением всех предпочтений и нюансов! 🎯 