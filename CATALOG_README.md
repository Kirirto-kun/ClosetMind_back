# 🛍️ Каталог магазинов и товаров

## 🚀 Быстрый запуск

```bash
# 1. Применить миграции
alembic upgrade head

# 2. Создать тестовые данные  
python scripts/seed_catalog.py

# 3. Запустить сервер
uvicorn src.main:app --reload

# 4. Протестировать
curl "http://localhost:8000/api/v1/stores/"
```

## 📋 Основные API

```bash
# Магазины
GET /api/v1/stores/                    # Все магазины
GET /api/v1/stores/cities              # Города
GET /api/v1/stores/{id}/products       # Товары магазина

# Товары  
GET /api/v1/products/                  # Все товары
GET /api/v1/products/categories        # Категории
GET /api/v1/products/?city=Москва      # По городу

# Отзывы
GET /api/v1/reviews/product/{id}       # Отзывы товара
POST /api/v1/reviews/            🔒    # Создать отзыв
```

## 🎯 Возможности

- **🏪 Магазины** - управление по городам
- **🔍 Поиск** - по названию, бренду, категории
- **📊 Фильтры** - город, цена, размеры, цвета
- **⭐ Рейтинги** - автоматический пересчет
- **🔄 Миграции** - безопасные изменения БД

## 📚 Документация

- **[CATALOG_SYSTEM_COMPLETE.md](./CATALOG_SYSTEM_COMPLETE.md)** - Полное описание
- **[CATALOG_API_DOCUMENTATION.md](./CATALOG_API_DOCUMENTATION.md)** - API документация  
- **[MIGRATIONS_GUIDE.md](./MIGRATIONS_GUIDE.md)** - Руководство по миграциям

## 🎉 Готово к использованию! 