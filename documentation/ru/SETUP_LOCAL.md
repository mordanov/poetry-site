# 🚀 Локальный запуск Poetry Site

Полная инструкция по запуску проекта на локальной машине.

## 📋 Требования

### Установленные системные пакеты:
- **Docker** & **Docker Compose** — для контейнеризации проекта
- **macOS/Linux/Windows** — система с поддержкой Docker

### Рекомендуемые версии:
- Docker: 20.10+
- Docker Compose: 1.29+ (или встроенный `docker compose`)

## 🔧 Установка

### 1️⃣ Клонирование репозитория

```bash
git clone <repository-url>
cd poetry-site
```

### 2️⃣ Настройка переменных окружения (опционально)

Создайте файл `.env` в корневой директории проекта для переопределения переменных:

```bash
# .env
POSTGRES_DB=poetry
POSTGRES_USER=poetry_user
POSTGRES_PASSWORD=change-me-poetry-db
DATABASE_URL=postgresql://poetry_user:change-me-poetry-db@db:5432/poetry

SECRET_KEY=your-secret-key-here-change-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme123
POET_NAME=Famous poet
```

Если файла нет, будут использованы значения по умолчанию из `docker-compose.yml`:
- `SECRET_KEY`: `change-this-secret-in-production`
- `ADMIN_USERNAME`: `admin`
- `ADMIN_PASSWORD`: `changeme123`

## ▶️ Запуск проекта

### Способ 1: Docker Compose (рекомендуется)

```bash
# Запуск всех контейнеров (db, backend, frontend)
docker-compose up

# Запуск в фоне
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

### Способ 2: Пересборка образов (если были изменения)

```bash
docker-compose up --build

# Или пересборка без кеша
docker-compose up --build --no-cache
```

## 🌐 Доступ к сайту

После запуска проект доступен по адресу:

```
http://localhost:8080
```

### Ключевые эндпоинты:

| URL | Описание |
|-----|---------|
| `http://localhost:8080` | Главная страница (Home) |
| `http://localhost:8080/poems` | Страница со всеми стихами |
| `http://localhost:8080/about` | Страница "Об авторе" |
| `http://localhost:8080/admin` | Администраторская панель |
| `http://localhost:8080/api/health` | Проверка здоровья API |

## 🔐 Вход в админ-панель

1. Перейдите на `http://localhost:8080`
2. Нажмите кнопку "Login" в правом верхнем углу
3. Введите учётные данные:
   - **Username**: `admin` (или из `.env`)
   - **Password**: `changeme123` (или из `.env`)

После входа вам станут доступны:
- ✏️ Создание и редактирование стихов
- 📝 Редактирование страницы "Об авторе"
- 🔐 Смена пароля

## 🌍 Многоязычность (i18n)

Сайт поддерживает **2 языка**:
- 🇬🇧 **Английский** (EN) — язык по умолчанию
- 🇷🇺 **Русский** (RU)

### Переключение языков:

1. В правом верхнем углу навигации найдите блок языков `EN | RU`
2. Нажмите на нужный язык
3. Выбранный язык сохраняется в `localStorage`

### Поддерживаемые переводы:

Все элементы интерфейса переведены:
- Навигация
- Заголовки и подзаголовки
- Кнопки и формы
- Сообщения об ошибках
- Администраторская панель

Словарь переводов находится в `/frontend/static/js/app.js` в переменной `I18N`.

## 📁 Структура проекта

```
poetry-site/
├── backend/                 # FastAPI приложение
│   ├── main.py             # Точка входа API
│   ├── database.py         # Инициализация БД PostgreSQL
│   ├── requirements.txt     # Python зависимости
│   ├── Dockerfile          # Docker образ для backend
│   └── routers/            # API маршруты
│       ├── auth.py         # Аутентификация (JWT)
│       ├── poems.py        # CRUD стихов
│       ├── comments.py     # Комментарии/размышления
│       └── about.py        # Страница об авторе
├── frontend/               # Статические файлы
│   ├── templates/
│   │   └── index.html      # Основной HTML (SPA)
│   └── static/
│       ├── css/
│       │   └── style.css   # Стили (классический дизайн)
│       └── js/
│           └── app.js      # SPA логика, i18n, маршрутизация
├── nginx/                  # Web сервер
│   ├── Dockerfile          # Docker образ для nginx
│   ├── default.conf        # Конфигурация nginx
│   └── default-https.conf  # HTTPS конфиг для продакшена
├── docker-compose.yml      # Оркестрация контейнеров
└── README.md              # Документация
```

## 🛠️ Разработка

### Внесение изменений в Backend

При изменении `/backend` файлов:

```bash
# Пересоберите образ backend
docker-compose build backend

# Перезапустите контейнер
docker-compose up backend
```

### Внесение изменений в Frontend

Изменения в `/frontend` применяются **автоматически**, так как файлы монтированы через volume:

```yaml
volumes:
  - ./frontend/templates/index.html:/var/www/html/index.html:ro
  - ./frontend/static:/var/www/html/static:ro
```

Просто обновите файлы и обновите браузер (Cmd+R / Ctrl+R).

### Добавление нового перевода

1. Откройте `/frontend/static/js/app.js`
2. Найдите переменную `I18N`
3. Добавьте новые ключи в оба словаря (`en` и `ru`):

```javascript
I18N = {
  en: {
    'my.key': 'English text',
    // ...
  },
  ru: {
    'my.key': 'Русский текст',
    // ...
  }
}
```

4. В HTML используйте атрибут `data-i18n`:

```html
<button data-i18n="my.key">Button</button>
```

5. В JavaScript используйте функцию `t()`:

```javascript
console.log(t('my.key')); // Выведет текст на текущем языке
```

## 📊 База данных

**Тип БД**: PostgreSQL (`db:5432`, БД `poetry`)

### Структура таблиц:

- **admin** — учётные данные администратора
- **poems** — стихотворения
- **tags** — теги для стихов
- **poem_tags** — связь между стихами и тегами
- **comments** — комментарии читателей
- **about** — страница "Об авторе"

Схема автоматически инициализируется при первом запуске в файле `/backend/database.py`.

## 🐛 Решение проблем

### Проблема: `port 80 is already in use`

Решение:
```bash
# Измените порт в docker-compose.yml
ports:
  - "8080:80"   # Используйте 8080 вместо 80
  - "8443:443"  # Используйте 8443 вместо 443
```

Затем откройте `http://localhost:8080`

### Проблема: Backend не запускается

```bash
# Проверьте логи
docker-compose logs backend

# Пересоберите образ
docker-compose build --no-cache backend
docker-compose up backend
```

### Проблема: БД повреждена

```bash
# Удалите volume и пересоздайте
docker-compose down -v
docker-compose up
```

### Проблема: Забыли пароль админа

```bash
# Удалите volume с данными БД
docker-compose down -v

# Пересоздайте с новыми учётными данными
echo "ADMIN_PASSWORD=newpassword123" > .env
docker-compose up
```

## 📚 API документация

Интерактивная документация доступна по адресу:

```
http://localhost/api/docs (Swagger UI)
http://localhost/api/redoc (ReDoc)
```

## 🚀 Развёртывание на продакшене

Для развёртывания используйте:

1. **Let's Encrypt** для SSL сертификатов (certbot)
2. **HTTPS конфиг** (`/nginx/default-https.conf`)
3. **Переменные окружения** в `.env` с безопасными значениями
4. **Обратный прокси** (nginx) для распределения трафика

Детали смотрите в `/nginx/default-https.conf` и `docker-compose.yml`.

## 📝 Лицензия

MIT

---

**Нужна помощь?** Проверьте логи контейнеров:
```bash
docker-compose logs --tail=50 backend
docker-compose logs --tail=50 nginx
```
