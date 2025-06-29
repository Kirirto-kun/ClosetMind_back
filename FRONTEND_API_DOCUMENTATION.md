# ClosetMind Chat API - Полная документация для фронтенда

## 🎯 Обзор системы

ClosetMind использует многоагентную AI-систему на базе **PydanticAI** с тремя специализированными агентами:

1. **Search Agent** - поиск товаров в интернете
2. **Outfit Agent** - рекомендации нарядов из гардероба пользователя  
3. **General Agent** - общие вопросы и беседа

**Координатор** автоматически определяет тип запроса и направляет его к нужному агенту.

---

## 🔐 Аутентификация

Все запросы требуют **Bearer токен** в заголовке:
```
Authorization: Bearer <your_jwt_token>
```

---

## 📡 API Endpoints

### Base URL: `/api/v1`

## 💬 Chat Management

### 1. Создать новый чат
```http
POST /api/v1/chats/
```

**Request Body:**
```json
{
  "title": "Мой новый чат"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Мой новый чат",
  "user_id": 123,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 2. Получить все чаты пользователя
```http
GET /api/v1/chats/
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Поиск одежды",
    "user_id": 123,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:45:00Z"
  },
  {
    "id": 2,
    "title": "Стильные образы",
    "user_id": 123,
    "created_at": "2024-01-14T15:20:00Z",
    "updated_at": "2024-01-14T16:10:00Z"
  }
]
```

### 3. Получить чат с сообщениями
```http
GET /api/v1/chats/{chat_id}
```

**Response:**
```json
{
  "id": 1,
  "title": "Поиск одежды",
  "user_id": 123,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:45:00Z",
  "messages": [
    {
      "id": 1,
      "content": "Найди мне черную футболку",
      "role": "user",
      "chat_id": 1,
      "created_at": "2024-01-15T10:31:00Z"
    },
    {
      "id": 2,
      "content": "{\"result\": {\"products\": [...]}}",
      "role": "assistant",
      "chat_id": 1,
      "created_at": "2024-01-15T10:31:30Z"
    }
  ]
}
```

### 4. Отправить сообщение в чат
```http
POST /api/v1/chats/{chat_id}/messages
```

**Request Body:**
```json
{
  "message": "Найди мне красивое платье для свидания"
}
```

**Response:**
```json
{
  "id": 3,
  "content": "{\"result\": {\"products\": [...]}}",
  "role": "assistant", 
  "chat_id": 1,
  "created_at": "2024-01-15T10:32:00Z"
}
```

### 5. Получить сообщения чата
```http
GET /api/v1/chats/{chat_id}/messages
```

**Response:**
```json
[
  {
    "id": 1,
    "content": "Что мне надеть сегодня?",
    "role": "user",
    "chat_id": 1,
    "created_at": "2024-01-15T10:31:00Z"
  },
  {
    "id": 2,
    "content": "{\"result\": {\"outfit_description\": \"...\"}}",
    "role": "assistant",
    "chat_id": 1,
    "created_at": "2024-01-15T10:31:30Z"
  }
]
```

### 6. Удалить чат
```http
DELETE /api/v1/chats/{chat_id}
```

**Response:**
```json
{
  "message": "Chat deleted successfully"
}
```

---

## 🤖 Структуры ответов агентов

### ⚠️ ВАЖНО: Парсинг ответов
Ответы от агентов приходят в поле `content` как **JSON-строка**. Фронтенд должен:

1. Распарсить JSON: `JSON.parse(message.content)`
2. Проверить тип в `result`
3. Отобразить соответствующий UI

### 1. Search Agent - Поиск товаров

**Триггеры:** "найди", "купить", "где купить", "поиск", "товар", "магазин"

**Структура ответа:**
```json
{
  "result": {
    "products": [
      {
        "name": "Черная футболка Uniqlo",
        "price": "1299 ₽",
        "description": "Базовая хлопковая футболка, идеальна для повседневной носки",
        "link": "https://www.uniqlo.com/ru/products/..."
      },
      {
        "name": "Nike Dri-FIT футболка",
        "price": "$29.99",
        "description": "Спортивная футболка с технологией отвода влаги",
        "link": "https://www.nike.com/products/..."
      }
    ]
  }
}
```

**UI компоненты для отображения:**
- Карточки товаров с изображениями
- Название, цена, описание
- Кнопка "Перейти в магазин" (link)
- Сетка товаров

### 2. Outfit Agent - Рекомендации нарядов

**Триггеры:** "что надеть", "образ", "наряд", "стиль", "гардероб", "одежда"

**Структура ответа:**
```json
{
  "result": {
    "outfit_description": "Стильный повседневный образ для прогулки по городу",
    "items": [
      {
        "name": "Белая рубашка",
        "category": "Рубашки",
        "image_url": "https://example.com/shirt.jpg"
      },
      {
        "name": "Синие джинсы",
        "category": "Брюки",
        "image_url": "https://example.com/jeans.jpg"
      },
      {
        "name": "Белые кроссовки",
        "category": "Обувь", 
        "image_url": "https://example.com/sneakers.jpg"
      }
    ],
    "reasoning": "Эти вещи отлично сочетаются: белый и синий - классическое сочетание, а белые кроссовки добавляют образу современности"
  }
}
```

**UI компоненты для отображения:**
- Заголовок с описанием образа
- Сетка вещей с изображениями
- Блок с объяснением выбора
- Возможность сохранить образ

### 3. General Agent - Общие вопросы

**Триггеры:** все остальные запросы

**Структура ответа:**
```json
{
  "result": {
    "response": "Искусственный интеллект (ИИ) - это область компьютерных наук, которая занимается созданием систем, способных выполнять задачи, обычно требующие человеческого интеллекта."
  }
}
```

**UI компоненты для отображения:**
- Обычное текстовое сообщение
- Markdown поддержка (опционально)

---

## 🔧 Альтернативный endpoint (без чата)

### Прямое обращение к агенту
```http
POST /api/v1/agent/chat
```

**Request Body:**
```json
{
  "message": "Найди мне зимнюю куртку"
}
```

**Response:**
```json
{
  "response": "{\"result\": {\"products\": [...]}}"
}
```

---

## 📝 Примеры запросов для тестирования

### Поиск товаров:
- "Найди мне черную футболку"
- "Где купить зимнюю куртку?"
- "Покажи красивые платья для свидания"
- "Ищу кроссовки Nike"

### Рекомендации нарядов:
- "Что мне надеть сегодня?"
- "Подбери образ для работы"
- "Стильный наряд для вечеринки"
- "Что носить в дождливую погоду?"

### Общие вопросы:
- "Что такое искусственный интеллект?"
- "Расскажи о моде"
- "Как ухаживать за одеждой?"
- "Привет, как дела?"

---

## 🎨 Рекомендации по UX

### Для поиска товаров:
- Показывать загрузку при поиске
- Карточки товаров с hover эффектами
- Фильтры по цене/категории
- Кнопка "В избранное"

### Для рекомендаций нарядов:
- Визуальная подборка с изображениями
- Возможность заменить вещь
- Сохранение понравившихся образов
- Календарь образов

### Для общих ответов:
- Поддержка форматирования текста
- Быстрые ответы/предложения
- История чатов

---

## ⚠️ Обработка ошибок

### Возможные ошибки:

```json
{
  "detail": "Chat not found"
}
```

```json
{
  "detail": "Failed to process message: Connection timeout"
}
```

```json
{
  "detail": "Unauthorized"
}
```

### HTTP коды:
- `200` - Успех
- `404` - Чат не найден
- `401` - Не авторизован
- `500` - Ошибка сервера

---

## 🔄 Workflow для фронтенда

1. **Авторизация** → получение JWT токена
2. **Создание чата** → `POST /api/v1/chats/`
3. **Отправка сообщения** → `POST /api/v1/chats/{chat_id}/messages`
4. **Парсинг ответа** → `JSON.parse(response.content)`
5. **Определение типа** → проверка структуры `result`
6. **Отображение UI** → соответствующие компоненты

---

## 🚀 Готовые компоненты для реализации

1. **ChatList** - список чатов
2. **ChatWindow** - окно чата с сообщениями  
3. **ProductCard** - карточка товара
4. **OutfitDisplay** - отображение образа
5. **MessageBubble** - пузырь сообщения
6. **LoadingSpinner** - индикатор загрузки

---

## 📱 Адаптивность

Система полностью готова для:
- Мобильных устройств
- Планшетов  
- Десктопа
- PWA приложений

Все ответы структурированы и готовы для любого типа интерфейса! 