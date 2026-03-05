# 📂 Структура проекта Poetry Site

Полное описание всех файлов и папок в проекте.

## 🏗️ Общая структура

```
poetry-site/
├── backend/                         # FastAPI приложение (API)
├── frontend/                        # Статические файлы (HTML, CSS, JS)
├── nginx/                           # Web сервер (обратный прокси)
├── docker-compose.yml               # Оркестрация контейнеров
├── SETUP_LOCAL.md                   # Инструкция по локальному запуску
├── I18N_GUIDE.md                    # Руководство по многоязычности
├── TESTING_GUIDE.md                 # Полное руководство по тестированию
└── README.md                        # Основная документация
```

## 📁 backend/ — FastAPI приложение

### backend/main.py
**Назначение:** Точка входа приложения, инициализация FastAPI.

**Что содержит:**
- Инициализация FastAPI приложения
- Настройка CORS (Cross-Origin Resource Sharing)
- Подключение всех маршрутов (routers)
- Lifespan контекст для инициализации БД

**Код:**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Инициализация БД при запуске
    yield

app = FastAPI(title="Poetry Site API", lifespan=lifespan)

# CORS — разрешить запросы со всех источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(poems.router, prefix="/api/poems", tags=["poems"])
app.include_router(about.router, prefix="/api/about", tags=["about"])
app.include_router(comments.router, prefix="/api/comments", tags=["comments"])
```

**Ключевые эндпоинты:**
- `GET /api/health` — проверка здоровья API

### backend/database.py
**Назначение:** Управление SQLite БД, инициализация таблиц.

**Что содержит:**
- Функция `get_db()` — получить подключение к БД
- Функция `init_db()` — создать таблицы и добавить начальные данные

**Таблицы:**
- **admin** — учётные данные администратора (username, password_hash)
- **about** — страница "Об авторе" (name, bio, photo_url)
- **poems** — стихотворения (title, body, created_at, updated_at)
- **tags** — теги (name)
- **poem_tags** — связь между стихами и тегами
- **comments** — комментарии читателей (poem_id, author, body)

**Пример использования:**
```python
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn  # Используется как dependency injection в FastAPI
    finally:
        conn.close()
```

### backend/requirements.txt
**Назначение:** Python зависимости для backend.

**Содержит:**
- `fastapi==0.111.0` — веб-фреймворк
- `uvicorn[standard]==0.29.0` — ASGI сервер
- `pyjwt==2.8.0` — JWT токены для аутентификации
- `bcrypt==4.1.3` — хеширование паролей
- `python-multipart==0.0.9` — парсинг form data
- `pydantic==2.7.1` — валидация данных

### backend/Dockerfile
**Назначение:** Сборка Docker образа для backend.

**Шаги:**
1. Используется базовый образ `python:3.12-slim`
2. Копируются requirements.txt и устанавливаются зависимости
3. Копируется весь код приложения
4. Создаётся директория `/data` для БД
5. Запускается Uvicorn сервер на порту 8000

### backend/routers/ — API маршруты

#### auth.py
**Назначение:** Аутентификация администратора.

**Эндпоинты:**
- `POST /api/auth/login` — вход администратора
  - Параметры: `username`, `password`
  - Ответ: `{"access_token": "...", "token_type": "bearer"}`
  
- `GET /api/auth/me` — получить информацию текущего администратора
  - Требуется токен
  - Ответ: `{"username": "admin"}`
  
- `POST /api/auth/change-password` — смена пароля
  - Требуется токен
  - Параметры: `current_password`, `new_password`

**Технология:** JWT (JSON Web Tokens)

#### poems.py
**Назначение:** CRUD операции со стихотворениями.

**Эндпоинты:**
- `GET /api/poems` — получить все стихотворения (с фильтром по тегам)
  - Query параметр: `tag` (опционально)
  - Ответ: список объектов со стихами и тегами
  
- `GET /api/poems/tags` — получить все теги со статистикой
  - Ответ: `[{"name": "love", "count": 5}, ...]`
  
- `GET /api/poems/{poem_id}` — получить одно стихотворение
  
- `POST /api/poems` — создать новое стихотворение
  - Требуется токен
  - Body: `{"title": "...", "body": "...", "tags": ["love", "nature"]}`
  
- `PUT /api/poems/{poem_id}` — обновить стихотворение
  - Требуется токен
  
- `DELETE /api/poems/{poem_id}` — удалить стихотворение
  - Требуется токен

#### comments.py
**Назначение:** Управление комментариями/размышлениями.

**Эндпоинты:**
- `GET /api/comments/{poem_id}` — получить все комментарии к стихотворению
  
- `POST /api/comments/{poem_id}` — добавить новый комментарий
  - Body: `{"author": "John", "body": "Beautiful poem!"}`
  
- `DELETE /api/comments/{comment_id}` — удалить комментарий
  - Требуется токен (только администратор)

#### about.py
**Назначение:** Управление страницей "Об авторе".

**Эндпоинты:**
- `GET /api/about` — получить информацию об авторе
  
- `PUT /api/about` — обновить информацию об авторе
  - Требуется токен
  - Body: `{"name": "...", "bio": "...", "photo_url": "..."}`

## 📁 frontend/ — Статические файлы

### frontend/templates/index.html
**Назначение:** Единственный HTML файл (SPA - Single Page Application).

**Что содержит:**
- `<head>` — метаданные, шрифты Google Fonts, подключение CSS
- `<nav>` — навигация с меню и кнопками входа/выхода, переключатель языков
- `<main id="app">` — все страницы приложения (скрыты, показываются при навигации)
  - `#page-home` — главная страница
  - `#page-poems` — список стихотворений
  - `#page-poem` — одно стихотворение с комментариями
  - `#page-about` — страница об авторе
  - `#page-admin` — администраторская панель
- `#login-modal` — модальное окно входа
- `#toast` — всплывающие уведомления

**Структура меню:**

```html

<nav class="nav">
    <a href="/" class="nav-logo">L·G</a>
    <ul class="nav-links">
        <li><a href="/" data-page="home">Home</a></li>
        <li><a href="/poems" data-page="poems">Poems</a></li>
        <li><a href="/about" data-page="about">About</a></li>
        <li id="nav-admin-link"><a href="/admin" data-page="admin">Admin</a></li>
    </ul>
    <div class="nav-right">
        <span id="nav-login-btn" onclick="showLoginModal()">Login</span>
        <span id="nav-logout-btn" style="display:none" onclick="logout()">Logout</span>
        <div class="lang-switch">
            <button data-lang="en" class="lang-btn">EN</button>
            <button data-lang="ru" class="lang-btn">RU</button>
        </div>
    </div>
</nav>
```

### frontend/static/css/style.css
**Назначение:** Все стили приложения.

**Особенности:**
- **Классический дизайн:** шрифты Cormorant Garamond, IM Fell English
- **Цветовая схема:** чёрный (#1a1612), пергамент (#f5f0e8), золотой (#b8902a)
- **Текстура:** зерно (grain) на фоне для винтажного эффекта
- **Адаптивный дизайн:** работает на десктопе и мобиле
- **Анимации:** плавные переходы между страницами (fadeIn)

**Основные классы:**
- `.nav` — фиксированная навигация
- `.page` — контейнер страницы
- `.btn-primary`, `.btn-ghost` — стили кнопок
- `.hero` — главная секция
- `.poems-grid`, `.poems-list` — контейнеры стихов
- `.admin-panel` — админ панель
- `.lang-switch` — переключатель языков

**Переменные CSS (CSS custom properties):**
```css
:root {
  --ink: #1a1612;              /* Основной текст */
  --parchment: #f5f0e8;        /* Фон */
  --cream: #faf7f2;            /* Светлый фон */
  --gold: #b8902a;             /* Акцент */
  --rust: #8b3a2a;             /* Второй акцент */
  --muted: #7a6f62;            /* Приглушённый текст */
  --border: #ddd5c4;           /* Границы */
  --shadow: rgba(26,22,18,0.12); /* Тени */
}
```

### frontend/static/js/app.js
**Назначение:** Вся логика приложения.

**Размер:** ~680 строк кода

**Основные разделы:**

#### 1. I18N (Многоязычность)
```javascript
const I18N = {
  en: { /* 100+ ключей на английском */ },
  ru: { /* 100+ ключей на русском */ }
}

function t(key, vars = {})    // Получить перевод
function applyTranslations()   // Применить переводы
function setLanguage(lang)     // Сменить язык
```

#### 2. Маршрутизация
```javascript
function navigate(page, push = true, param = null)  // Переключить страницу
function handleRoute()                               // Обработать URL
```

#### 3. Аутентификация
```javascript
async function login(e)        // Вход администратора
function logout()              // Выход
function updateAuthUI()         // Обновить UI в зависимости от авторизации
```

#### 4. API Запросы
```javascript
async function apiFetch(path, opts = {})  // Обёртка fetch с авторизацией
```

#### 5. Загрузка данных
```javascript
async function loadHome()      // Загрузить главную страницу
async function loadPoems()     // Загрузить список стихов
async function loadAbout()     // Загрузить информацию об авторе
```

#### 6. CRUD Операции
```javascript
async function createPoem(...)  // Создать стихотворение
async function updatePoem(...)  // Обновить
async function deletePoem(...)  // Удалить
async function addComment(...)  // Добавить комментарий
```

**Состояние приложения:**
```javascript
let token = localStorage.getItem('token') || null;  // JWT токен
let currentTag = null;                              // Текущий фильтр по тегам
let editingPoemId = null;                           // ID редактируемого стиха
let currentLang = 'en' или 'ru';                   // Текущий язык
```

## 📁 nginx/ — Web сервер

### nginx/default.conf
**Назначение:** Конфигурация Nginx для локального развития.

**Что делает:**
1. **Слушает** порт 80 (HTTP)
2. **Раздаёт** статические файлы (CSS, JS, HTML)
3. **Проксирует** запросы `/api/*` на backend (port 8000)
4. **Реализует SPA routing** — все неизвестные маршруты перенаправляют на index.html
5. **Включает Gzip сжатие** для оптимизации

**Ключевые блоки:**
```nginx
# Раздача статических файлов
location /static/ {
    expires 7d;
    add_header Cache-Control "public, immutable";
}

# Проксирование API
location /api/ {
    proxy_pass http://backend:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_read_timeout 60s;
}

# SPA routing
location / {
    try_files $uri $uri/ /index.html;
}
```

### nginx/default-https.conf
**Назначение:** Конфигурация для продакшена с HTTPS.

**Особенности:**
- Слушает порты 80 и 443
- Переадресовывает HTTP на HTTPS
- Использует SSL сертификаты от Let's Encrypt (certbot)

### nginx/Dockerfile
**Назначение:** Построение Docker образа для Nginx.

**Шаги:**
1. Базовый образ: `nginx:alpine`
2. Копирует конфиг: `nginx/default.conf`
3. Копирует HTML: `frontend/templates/index.html`
4. Копирует статику: `frontend/static/*`

## 🐳 docker-compose.yml
**Назначение:** Оркестрация всех контейнеров.

**Сервисы:**
- **backend** — FastAPI приложение (порт 8000)
- **nginx** — Web сервер (порты 80, 443)
- **certbot** — Получение SSL сертификатов

**Volumes:**
- `poetry_data` — сохранение БД между запусками
- `certbot_certs` — сохранение SSL сертификатов
- `certbot_www` — директория для ACME challenge

**Переменные окружения:**
```yaml
DB_PATH=/data/poetry.db           # Путь к БД
SECRET_KEY=...                    # JWT секретный ключ
ADMIN_USERNAME=admin              # Логин администратора
ADMIN_PASSWORD=changeme123        # Пароль администратора
```

## 📄 Документационные файлы

### SETUP_LOCAL.md
Инструкция по локальному запуску (вы читаете это).

### I18N_GUIDE.md
Полное руководство по системе многоязычности.

### TESTING_GUIDE.md
Пошаговое руководство по тестированию всех функций.

### README.md
Основная документация проекта (описание, особенности, лицензия).

## 📊 Размер файлов

```
backend/main.py              36 lines   ~1 KB
backend/database.py          80 lines   ~3 KB
backend/routers/auth.py      65 lines   ~2 KB
backend/routers/poems.py     117 lines  ~4 KB
backend/routers/about.py     35 lines   ~1 KB
backend/routers/comments.py  46 lines   ~1.5 KB
frontend/templates/index.html 128 lines ~6 KB
frontend/static/css/style.css 542 lines ~15 KB
frontend/static/js/app.js    678 lines ~25 KB
```

**Итого:** ~60 KB чистого кода (без зависимостей)

## 🔄 Поток данных

```
┌─ Браузер ──────────────────────┐
│  - index.html                  │
│  - app.js (678 строк кода)     │
│  - style.css                   │
└─────────────────────────────────┘
           │
           │ HTTP запросы
           ▼
┌─ Nginx (обратный прокси) ──────┐
│ - Раздаёт статику              │
│ - Проксирует /api/* на backend  │
│ - Реализует SPA routing         │
└─────────────────────────────────┘
           │
           │ Проксирует API запросы
           ▼
┌─ FastAPI (Backend) ────────────┐
│ - main.py (точка входа)        │
│ - auth.py (JWT)                │
│ - poems.py (CRUD)              │
│ - comments.py                  │
│ - about.py                     │
└─────────────────────────────────┘
           │
           │ SQL запросы
           ▼
┌─ SQLite Database ──────────────┐
│ - /data/poetry.db              │
│ - 6 таблиц                     │
└─────────────────────────────────┘
```

---

**Нужна информация о конкретном файле?** Смотрите комментарии в самом коде!

