# Project Structure — Poetry Site

## Top-level
```
poetry-site/
├── backend/              # FastAPI API
├── frontend/             # HTML/CSS/JS SPA
├── nginx/                # Nginx config
├── documentation/        # Docs (RU/EN)
├── docker-compose.yml    # Local stack (backend + db + frontend)
├── .env.example          # Env template
└── README.md             # Root overview (EN)
```

## Backend highlights
- `backend/main.py` — FastAPI app, routes, static uploads
- `backend/database.py` — SQLAlchemy engine/session (`DATABASE_URL`)
- `backend/models.py` — ORM models (poems, tags, comments, versions)
- `backend/routers/` — auth, poems, comments, about

## Database
- PostgreSQL 16 service: `db`
- Connection configured via `DATABASE_URL`
- Upload files stored in `uploads_data` volume

## Frontend highlights
- `frontend/templates/index.html` — SPA shell
- `frontend/static/js/app.js` — routing + API calls + i18n
- `frontend/static/css/style.css` — UI styling

## Nginx
- `nginx/default.conf` — HTTP config
- `nginx/default-https.conf` — HTTPS config (certbot)

**Русская версия:** `documentation/ru/PROJECT_STRUCTURE.md`
