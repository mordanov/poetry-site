# poetry-site — Poetry Site

Легкий сайт для публикации стихов с админ-панелью, версиями, комментариями и загрузкой изображений.

## Возможности
- CRUD стихов с тегами и UUID-ссылками
- Черновики (видны только админу)
- Загрузка изображения на стих (JPG/PNG, до 1MB)
- История версий после редактирования
- Комментарии с датой и модерацией
- Пагинация списка стихов
- Экспорт/импорт ZIP (стихи + комментарии + изображения)
- Многоязычный интерфейс (EN/RU/ES/FR)

---

## Структура проекта

```
poetry-site/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # PostgreSQL setup & session management
│   ├── models.py            # SQLAlchemy ORM models
│   ├── requirements.txt
│   ├── Dockerfile
│   └── routers/
│       ├── auth.py          # JWT login, password change
│       ├── poems.py         # CRUD + tags + export/import + images
│       ├── about.py         # About page content
│       └── comments.py      # Guest comments
├── frontend/
│   ├── templates/
│   │   └── index.html       # Single-page app shell
│   └── static/
│       ├── css/style.css
│       └── js/app.js        # All routing & API calls
├── nginx/
│   ├── Dockerfile
│   ├── default.conf         # HTTP config
│   └── default-https.conf   # HTTPS config (after cert)
├── documentation/
│   ├── INDEX.md             # Documentation index
│   └── ...
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Локальный запуск (рекомендуется)

Запуск всего стека через Docker Compose:

```bash
cd /Users/aleksandr/Local/web-projects/poetry-site
docker-compose up
```

Откройте `http://localhost:8080`.

Если запускать backend напрямую — используйте те же переменные окружения, что и в Docker (`DATABASE_URL`, `UPLOADS_DIR`, `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`).

---

## Админ-панель

1. Откройте сайт и нажмите **Login**.
2. Введите учётные данные из `.env`.
3. Перейдите в **Admin**.

**Вкладка Poems:**
- Добавление/редактирование/удаление стихов
- Черновики видны только админу
- Загрузка одного изображения на стих (JPG/PNG, до 1MB)
- История версий
- **Export Poems** — ZIP со стихами, комментариями и изображениями
- **Import Poems** — импорт ZIP

**About Page:** имя, био, фото.

**Comments:** просмотр и удаление.

**Password:** смена пароля.

---

## API (избранное)

Все админ-эндпоинты требуют `Authorization: Bearer <token>`.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/login` | — | Get JWT token |
| POST | `/api/auth/change-password` | ✓ | Change password |
| GET | `/api/poems` | — | List poems (public only) |
| GET | `/api/poems/uuid/{uuid}` | — | Get poem by UUID |
| POST | `/api/poems` | ✓ | Create poem |
| PUT | `/api/poems/{id}` | ✓ | Update poem |
| DELETE | `/api/poems/{id}` | ✓ | Delete poem |
| POST | `/api/poems/{id}/image` | ✓ | Upload poem image |
| DELETE | `/api/poems/{id}/image` | ✓ | Remove poem image |
| GET | `/api/poems/export/poems` | ✓ | Export poems/comments/images ZIP |
| POST | `/api/poems/import` | ✓ | Import poems/comments/images ZIP |
| GET | `/api/comments/{poem_id}` | — | Get comments for poem |
| POST | `/api/comments/{poem_id}` | — | Add comment |
| DELETE | `/api/comments/{id}` | ✓ | Delete comment |

Interactive docs: `/api/docs` и `/api/redoc`.

---

## Документация

- Старт: `documentation/INDEX.md`
- EN версия: `documentation/INDEX.en.md`
- i18n: `documentation/I18N_GUIDE.md`
- Добавление языка: `documentation/ADD_NEW_LANGUAGE.md`
- Тестирование: `documentation/TESTING_GUIDE.md`
- Экспорт/импорт: `documentation/EXPORT_IMPORT_GUIDE.md`
