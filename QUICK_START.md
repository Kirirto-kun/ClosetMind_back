# 🚀 ClosetMind Chat API - Quick Start

## 📋 Краткая сводка для фронтенда

### 🎯 Что это такое?
Многоагентная AI-система с 3 специализированными агентами:
- **Search Agent** 🔍 - поиск товаров
- **Outfit Agent** 👔 - рекомендации нарядов  
- **General Agent** 💭 - общие вопросы

### 🔑 Ключевые моменты

#### 1. Авторизация
```javascript
headers: { Authorization: `Bearer ${token}` }
```

#### 2. Основные endpoints
```
POST /api/v1/chats/                    // Создать чат
GET  /api/v1/chats/                    // Список чатов
GET  /api/v1/chats/{id}                // Чат с сообщениями
POST /api/v1/chats/{id}/messages       // Отправить сообщение
DELETE /api/v1/chats/{id}              // Удалить чат
```

#### 3. ⚠️ ВАЖНО: Парсинг ответов агентов
Ответы приходят как JSON-строка в поле `content`:
```javascript
const response = JSON.parse(message.content);
const { result } = response;

// Проверяем тип ответа:
if ('products' in result) {
  // Search Agent - показываем карточки товаров
} else if ('outfit_description' in result) {
  // Outfit Agent - показываем образ
} else if ('response' in result) {
  // General Agent - показываем текст
}
```

### 📊 Структуры данных

#### Search Agent Response
```json
{
  "result": {
    "products": [
      {
        "name": "Черная футболка",
        "price": "1299 ₽", 
        "description": "Описание товара",
        "link": "https://shop.com/product"
      }
    ]
  }
}
```

#### Outfit Agent Response  
```json
{
  "result": {
    "outfit_description": "Стильный образ",
    "items": [
      {
        "name": "Белая рубашка",
        "category": "Рубашки",
        "image_url": "https://image.url"
      }
    ],
    "reasoning": "Почему этот образ работает"
  }
}
```

#### General Agent Response
```json
{
  "result": {
    "response": "Обычный текстовый ответ"
  }
}
```

### 🎨 UI Компоненты для реализации

1. **ChatList** - боковая панель с чатами
2. **ChatWindow** - окно чата с сообщениями
3. **ProductCard** - карточка товара с кнопкой в магазин
4. **OutfitDisplay** - отображение образа с вещами
5. **MessageBubble** - пузырь сообщения (user/assistant)

### 📱 Примеры запросов для тестирования

**Поиск товаров:**
- "Найди черную футболку"
- "Где купить зимнюю куртку?"

**Рекомендации нарядов:**
- "Что надеть сегодня?"
- "Подбери образ для работы"

**Общие вопросы:**
- "Что такое мода?"
- "Привет, как дела?"

### 🔄 Workflow

1. Авторизация → получение JWT
2. Создание чата → `POST /chats/`
3. Отправка сообщения → `POST /chats/{id}/messages`
4. Парсинг ответа → `JSON.parse(content)`
5. Отображение UI → соответствующий компонент

### 🛠️ Готовый код

Полные примеры компонентов смотри в `FRONTEND_EXAMPLES.md`

### 🚨 Частые ошибки

1. **Забыли распарсить JSON** - ответы агентов приходят как строка
2. **Неправильная авторизация** - нужен Bearer token
3. **Не проверили тип ответа** - нужно определить какой агент ответил

### ✅ Чек-лист готовности

- [ ] Настроена авторизация с Bearer token
- [ ] Реализован парсинг JSON ответов агентов
- [ ] Созданы компоненты для всех типов ответов
- [ ] Добавлена обработка ошибок
- [ ] Протестированы все типы запросов

**🎉 Готово! Система полностью функциональна и готова к использованию!** 