# API Каталога Магазинов и Товаров

## 🏪 Обзор

Система каталога магазинов и товаров предоставляет полнофункциональный API для:
- Управления магазинами по городам
- Каталога товаров с фильтрацией и поиском
- Системы отзывов и рейтингов
- Статистики и аналитики

## 📊 Структура данных

### Store (Магазин)
```json
{
  "id": 1,
  "name": "H&M",
  "description": "Fashion and quality at the best price",
  "city": "Москва",
  "logo_url": "https://example.com/logo.svg",
  "website_url": "https://hm.com",
  "rating": 4.2,
  "total_products": 1250,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Product (Товар)
```json
{
  "id": 1,
  "name": "Cotton T-Shirt",
  "description": "Classic cotton t-shirt with round neck",
  "price": 29.99,
  "original_price": 39.99,
  "category": "Одежда",
  "brand": "H&M",
  "sizes": ["S", "M", "L", "XL"],
  "colors": ["white", "black", "blue"],
  "image_urls": ["https://example.com/tshirt1.jpg"],
  "rating": 4.5,
  "reviews_count": 123,
  "stock_quantity": 150,
  "is_active": true,
  "discount_percentage": 25.0,
  "is_in_stock": true,
  "store": {
    "id": 1,
    "name": "H&M",
    "city": "Москва",
    "logo_url": "https://example.com/logo.svg",
    "rating": 4.2
  },
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Review (Отзыв)
```json
{
  "id": 1,
  "product_id": 1,
  "rating": 5,
  "comment": "Отличное качество, рекомендую!",
  "user": {
    "id": 1,
    "username": "user123"
  },
  "is_verified": true,
  "rating_stars": "⭐⭐⭐⭐⭐",
  "created_at": "2024-01-01T00:00:00Z"
}
```

## 🏪 API Магазинов

### GET /api/v1/stores/
Получить список всех магазинов с фильтрацией

**Параметры:**
- `city` (optional) - Фильтр по городу
- `rating_min` (optional) - Минимальный рейтинг
- `sort_by` (optional) - Сортировка: name, rating, city, created_at
- `sort_order` (optional) - Порядок: asc, desc
- `page` (optional, default=1) - Номер страницы
- `per_page` (optional, default=20) - Количество на странице

**Пример:**
```bash
GET /api/v1/stores/?city=Москва&rating_min=4.0&sort_by=rating&sort_order=desc
```

**Ответ:**
```json
{
  "stores": [...],
  "total": 15,
  "page": 1,
  "per_page": 20
}
```

### GET /api/v1/stores/cities
Получить список всех городов с магазинами

**Ответ:**
```json
{
  "cities": [
    {
      "city": "Москва",
      "stores_count": 15,
      "products_count": 12450
    }
  ]
}
```

### GET /api/v1/stores/by-city/{city}
Получить магазины по городу

### GET /api/v1/stores/{store_id}
Получить информацию о конкретном магазине

### GET /api/v1/stores/{store_id}/products
Получить товары конкретного магазина

**Параметры:**
- `category` (optional) - Фильтр по категории
- `in_stock_only` (optional) - Только товары в наличии
- `sort_by` (optional) - Сортировка
- `sort_order` (optional) - Порядок
- `page`, `per_page` - Пагинация

### GET /api/v1/stores/{store_id}/stats
Получить статистику магазина

**Ответ:**
```json
{
  "id": 1,
  "name": "H&M",
  "city": "Москва",
  "total_products": 1250,
  "active_products": 1200,
  "average_rating": 4.2,
  "total_reviews": 5678,
  "categories_count": 8,
  "top_categories": ["Одежда", "Обувь", "Аксессуары"]
}
```

### POST /api/v1/stores/ 🔒
Создать новый магазин (требует авторизации)

### PUT /api/v1/stores/{store_id} 🔒
Обновить магазин (требует авторизации)

## 🛍️ API Товаров

### GET /api/v1/products/
Получить список товаров с мощной фильтрацией

**Параметры фильтрации:**
- `query` - Текстовый поиск по названию, описанию, бренду
- `category` - Фильтр по категории
- `city` - Фильтр по городу магазина
- `store_id` - Фильтр по магазину
- `brand` - Фильтр по бренду
- `min_price`, `max_price` - Диапазон цен
- `min_rating` - Минимальный рейтинг
- `sizes` - Размеры через запятую (S,M,L)
- `colors` - Цвета через запятую
- `in_stock_only` - Только товары в наличии

**Параметры сортировки:**
- `sort_by` - name, price, rating, created_at
- `sort_order` - asc, desc

**Примеры:**
```bash
# Поиск футболок в Москве
GET /api/v1/products/?query=футболка&city=Москва

# Товары до 3000 рублей с рейтингом от 4.0
GET /api/v1/products/?max_price=3000&min_rating=4.0

# Одежда размеров M и L в наличии
GET /api/v1/products/?category=Одежда&sizes=M,L&in_stock_only=true
```

### GET /api/v1/products/categories
Получить список всех категорий с статистикой

**Ответ:**
```json
{
  "categories": [
    {
      "category": "Одежда",
      "products_count": 1500,
      "avg_price": 2500.0,
      "top_brands": ["H&M", "Zara", "Uniqlo"]
    }
  ]
}
```

### GET /api/v1/products/by-city/{city}
Получить товары по городу

### GET /api/v1/products/search
Расширенный поиск товаров (POST с JSON телом)

**Тело запроса:**
```json
{
  "query": "футболка",
  "category": "Одежда",
  "city": "Москва",
  "min_price": 500,
  "max_price": 2000,
  "sizes": ["S", "M"],
  "in_stock_only": true,
  "sort_by": "price",
  "sort_order": "asc",
  "page": 1,
  "per_page": 20
}
```

### GET /api/v1/products/{product_id}
Получить детальную информацию о товаре

### POST /api/v1/products/ 🔒
Создать новый товар (требует авторизации)

### PUT /api/v1/products/{product_id} 🔒
Обновить товар (требует авторизации)

## ⭐ API Отзывов

### GET /api/v1/reviews/product/{product_id}
Получить отзывы для товара

**Параметры:**
- `rating_filter` (optional) - Фильтр по рейтингу (1-5)
- `verified_only` (optional) - Только проверенные отзывы
- `sort_by` (optional) - created_at, rating
- `sort_order` (optional) - asc, desc
- `page`, `per_page` - Пагинация

**Ответ:**
```json
{
  "reviews": [...],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "average_rating": 4.3,
  "rating_distribution": {
    "5": 80,
    "4": 45,
    "3": 20,
    "2": 3,
    "1": 2
  }
}
```

### GET /api/v1/reviews/user/{user_id}
Получить отзывы пользователя

### POST /api/v1/reviews/ 🔒
Создать отзыв (требует авторизации)

**Тело запроса:**
```json
{
  "product_id": 1,
  "rating": 5,
  "comment": "Отличное качество!"
}
```

### PUT /api/v1/reviews/{review_id} 🔒
Обновить свой отзыв (требует авторизации)

### DELETE /api/v1/reviews/{review_id} 🔒
Удалить свой отзыв (требует авторизации)

### GET /api/v1/reviews/stats/product/{product_id}
Получить статистику отзывов для товара

## 🔍 Примеры использования

### 1. Получить все магазины в Москве
```bash
curl -X GET "http://localhost:8000/api/v1/stores/?city=Москва"
```

### 2. Найти товары H&M до 2000 рублей
```bash
curl -X GET "http://localhost:8000/api/v1/products/?brand=H%26M&max_price=2000"
```

### 3. Получить товары категории "Одежда" в наличии
```bash
curl -X GET "http://localhost:8000/api/v1/products/?category=Одежда&in_stock_only=true"
```

### 4. Поиск по тексту с сортировкой по цене
```bash
curl -X GET "http://localhost:8000/api/v1/products/?query=футболка&sort_by=price&sort_order=asc"
```

### 5. Получить статистику по городам
```bash
curl -X GET "http://localhost:8000/api/v1/stores/cities"
```

### 6. Получить категории товаров
```bash
curl -X GET "http://localhost:8000/api/v1/products/categories"
```

## 🔒 Авторизация

Для операций создания/обновления требуется JWT токен:

```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Новый товар",
    "price": 1999.0,
    "category": "Одежда",
    "store_id": 1
  }'
```

## 📱 Коды ответов

- `200 OK` - Успешный запрос
- `201 Created` - Успешное создание
- `400 Bad Request` - Ошибка валидации
- `401 Unauthorized` - Требуется авторизация
- `403 Forbidden` - Недостаточно прав
- `404 Not Found` - Ресурс не найден
- `422 Unprocessable Entity` - Ошибка валидации данных

## 🚀 Тестовые данные

Для быстрого тестирования используйте:

```bash
# Создать тестовые данные
python scripts/seed_catalog.py

# Очистить тестовые данные
python scripts/seed_catalog.py --clear
```

## 🔄 Пагинация

Все списочные endpoints поддерживают пагинацию:

```json
{
  "data": [...],
  "total": 500,
  "page": 1,
  "per_page": 20
}
```

## 🎯 Особенности

- **Полнотекстовый поиск** по названию, описанию, бренду
- **Фильтрация по городам** магазинов
- **Система рейтингов** с автоматическим пересчетом
- **Поддержка скидок** с отображением процента
- **Управление запасами** с проверкой наличия
- **Векторизация товаров** для семантического поиска (готово к интеграции)
- **Статистика и аналитика** по магазинам и товарам

## 📄 Документация API

Полная интерактивная документация доступна по адресу:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 