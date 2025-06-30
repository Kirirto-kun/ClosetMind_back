# Быстрый старт с миграциями

## 🚀 Основные команды

```bash
# Применить все миграции
alembic upgrade head

# Создать новую миграцию после изменения моделей
alembic revision --autogenerate -m "Описание изменений"

# Откатить последнюю миграцию
alembic downgrade -1

# Посмотреть текущую версию БД
alembic current

# Посмотреть историю миграций
alembic history
```

## 📝 Рабочий процесс

1. **Изменяете модель** в `src/models/`
2. **Создаёте миграцию**: `alembic revision --autogenerate -m "Описание"`
3. **Проверяете файл миграции** в `alembic/versions/`
4. **Применяете**: `alembic upgrade head`

## ⚠️ Важно

- **Всегда проверяйте** автогенерированные миграции перед применением
- **Делайте бэкап** перед применением на продакшене
- **Тестируйте откат**: `alembic downgrade -1` → `alembic upgrade head`

## 🐳 Docker

Для автоматического применения миграций при запуске контейнера добавьте в команду:

```bash
alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## 📚 Документация

Подробное руководство: [MIGRATIONS_GUIDE.md](./MIGRATIONS_GUIDE.md) 