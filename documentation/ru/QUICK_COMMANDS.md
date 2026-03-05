# ⚡ Быстрые команды для работы с Poetry Site

Шпаргалка с наиболее полезными командами для запуска, разработки и отладки проекта.

## 🚀 Базовые команды

### Запуск проекта

```bash
# Простой запуск (видны логи)
docker-compose up

# Запуск в фоне
docker-compose up -d

# Запуск с пересборкой образов
docker-compose up --build

# Пересборка без кеша
docker-compose up --build --no-cache
```

### Остановка проекта

```bash
# Остановить контейнеры (сохранить данные)
docker-compose down

# Остановить всё и удалить БД/volumes
docker-compose down -v

# Перезагрузить контейнеры
docker-compose restart
```

## 📊 Просмотр логов

```bash
# Все логи
docker-compose logs

# Логи backend
docker-compose logs backend

# Логи nginx
docker-compose logs nginx

# Логи в реальном времени
docker-compose logs -f

# Последние 50 строк
docker-compose logs --tail=50

# Логи backend в реальном времени (полезно для разработки)
docker-compose logs -f backend
```

## 🔧 Работа с контейнерами

### Вход в контейнер

```bash
# Bash в backend контейнере
docker-compose exec backend bash

# Bash в nginx контейнере
docker-compose exec nginx bash

# Python интерпретатор в backend
docker-compose exec backend python3
```

### Управление контейнерами

```bash
# Статус контейнеров
docker-compose ps

# Перестартовать backend
docker-compose restart backend

# Остановить nginx (оставить backend)
docker-compose stop nginx

# Запустить только backend
docker-compose up backend
```

## 💾 Работа с БД

```bash
# Открыть SQLite консоль
docker-compose exec backend sqlite3 /data/poetry.db

# Внутри sqlite3:
# Показать таблицы
.tables

# Показать схему таблицы
.schema poems

# Выборка всех стихов
SELECT * FROM poems;

# Выборка администратора
SELECT * FROM admin;

# Выход из sqlite3
.exit

# Одноразовый SQL запрос
docker-compose exec backend sqlite3 /data/poetry.db "SELECT COUNT(*) FROM poems;"

# Сохранение БД в файл (для бекапа)
docker-compose exec backend bash -c "sqlite3 /data/poetry.db '.dump' > /tmp/backup.sql"
```

## 🌐 Тестирование API

```bash
# Проверка здоровья API
curl http://localhost/api/health

# Получить все стихи
curl http://localhost/api/poems

# Получить информацию об авторе
curl http://localhost/api/about

# Получить все теги
curl http://localhost/api/poems/tags

# Попытка создания стиха (без токена, должна ошибка 401)
curl -X POST http://localhost/api/poems \
  -H "Content-Type: application/json" \
  -d '{"title":"test","body":"test"}'

# Вход администратора
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=changeme123"

# Сохранение токена в переменную
TOKEN=$(curl -s -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=changeme123" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

# Использование токена для защищённого запроса
curl -X GET http://localhost/api/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Создание стиха с использованием токена
curl -X POST http://localhost/api/poems \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Poem","body":"Beautiful verse","tags":["love"]}'
```

## 🧹 Очистка и переустановка

```bash
# Полная очистка (удалить ВСЁ)
docker-compose down -v && docker system prune -a

# Удалить только БД (сохранить код)
docker volume rm poetry-site_poetry_data

# Пересоздать БД (запустит инициализацию)
docker-compose down -v
docker-compose up

# Пересоздать только backend образ
docker-compose build --no-cache backend

# Удалить конкретный контейнер
docker-compose rm backend

# Посмотреть размер volumes
docker system df

# Очистить неиспользуемые образы
docker image prune -a
```

## 📁 Файловая система

```bash
# Посмотреть содержимое контейнера
docker-compose exec backend ls -la /app

# Посмотреть содержимое /data
docker-compose exec backend ls -la /data

# Просмотреть конкретный файл
docker-compose exec backend cat /app/main.py

# Скопировать файл из контейнера
docker cp poetry-site-backend-1:/data/poetry.db ./poetry_backup.db

# Скопировать файл в контейнер
docker cp ./my_file.txt poetry-site-backend-1:/data/my_file.txt
```

## 🔐 Работа с окружением

```bash
# Посмотреть переменные окружения контейнера
docker-compose exec backend env | sort

# Установить переменную в .env файле
echo "SECRET_KEY=my-secret-key" >> .env

# Перезагрузить после изменения .env
docker-compose down
docker-compose up --build

# Проверить переменные в контейнере
docker-compose exec backend echo $DB_PATH
docker-compose exec backend echo $SECRET_KEY
```

## 🧪 Быстрое тестирование

```bash
# Проверка всех основных эндпоинтов
./test.sh

# Или вручную:
echo "🏥 Проверка здоровья..."
curl http://localhost/api/health && echo ""

echo "📖 Проверка стихов..."
curl http://localhost/api/poems && echo ""

echo "👤 Проверка об авторе..."
curl http://localhost/api/about && echo ""

echo "✅ Все проверки пройдены!"
```

## 🎯 Для разработчиков

```bash
# Пересборка backend при изменении кода Python
docker-compose build backend && docker-compose up backend

# Frontend изменяется горячо, просто обновите браузер (F5)

# Просмотр изменений в реальном времени
watch "docker-compose logs --tail=20 backend"

# Отладка Python (добавьте breakpoint() в код)
docker-compose exec backend python -m pdb main.py

# Просмотр использования ресурсов
docker stats

# Просмотр сетевых подключений контейнеров
docker network inspect poetry-site_default
```

## 🌐 Браузер и FrontEnd

```bash
# Откройте в браузере:
http://localhost              # Главная страница
http://localhost/admin        # Админ-панель (требует вход)
http://localhost/api/docs     # Swagger документация
http://localhost/api/redoc    # ReDoc документация

# Проверка консоли браузера (F12 → Console)
# Проверка сетевых запросов (F12 → Network)
# Проверка localStorage (F12 → Application → Local Storage)

# Посмотреть сохранённый токен
localStorage.getItem('token')

# Посмотреть выбранный язык
localStorage.getItem('lang')

# Очистить localStorage (выход)
localStorage.clear()
```

## 🐛 Решение проблем

```bash
# Проверка: сервис слушает портом?
lsof -i :80      # Nginx
lsof -i :8000    # Backend

# Если порт занят, найдите процесс
ps aux | grep docker

# Перезагрузка Docker
# macOS:
open -a Docker

# Linux:
sudo systemctl restart docker

# Проверка логов на ошибки
docker-compose logs | grep -i error
docker-compose logs | grep -i failed
docker-compose logs | grep -i exception

# Восстановление после сбоя
docker-compose down
docker-compose up --remove-orphans

# Проверка целостности БД
docker-compose exec backend sqlite3 /data/poetry.db "PRAGMA integrity_check;"
```

## 📈 Мониторинг производительности

```bash
# Просмотр использования памяти
docker stats --no-stream

# Просмотр дискового пространства
docker system df

# Медленные запросы к БД (примерный способ)
# Добавьте в Python code: import time; start=time.time(); ...; print(f"Query took {time.time()-start}s")

# Анализ кеша Docker
docker buildx du
```

## 📝 Одна команда для проверки всего

```bash
# Скопируйте и запустите:
echo "=== DOCKER STATUS ===" && \
docker-compose ps && \
echo "" && \
echo "=== API HEALTH ===" && \
curl -s http://localhost/api/health && echo "" && \
echo "" && \
echo "=== RECENT LOGS ===" && \
docker-compose logs --tail=5 backend && \
echo "" && \
echo "✅ Проверка завершена!"
```

## 🚀 Как использовать эти команды

### 1. Создайте файл `commands.sh`

```bash
#!/bin/bash
# Добавьте нужные команды из этого файла

# Например, быстрая проверка:
docker-compose logs backend | tail -20
```

### 2. Сделайте файл исполняемым

```bash
chmod +x commands.sh
./commands.sh
```

### 3. Добавьте в `.bashrc` или `.zshrc` (для macOS)

```bash
# ~/.zshrc
alias poetry-logs="docker-compose logs -f backend"
alias poetry-up="docker-compose up -d"
alias poetry-down="docker-compose down"
alias poetry-test="curl http://localhost/api/health"
```

Тогда можно использовать: `poetry-logs`, `poetry-up` и т.д.

---

**Нужна помощь?** Проверьте секцию "Решение проблем" или посмотрите `docker-compose logs`.

**Счастливой работы! 🎉**

