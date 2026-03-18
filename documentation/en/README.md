# poetry-site — Poetry Site

Personal poetry site for poetry-site. Built with **FastAPI** backend, **Vanilla JS** SPA frontend, **PostgreSQL** database, served via **Nginx**, deployed with **Docker Compose**.

## Features
- Poem CRUD with tags and UUID-based public links
- Draft mode for admin-only visibility
- Image upload per poem (JPG/PNG, max 1MB)
- Version history for poem edits
- Comments with timestamps and admin moderation
- Pagination on public poems list
- Export/import as ZIP (poems + comments + images)
- Multi-language UI (EN/RU/ES/FR)

---

## Project Structure

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

## Local Development (Recommended)

Run the full stack with Docker Compose:

```bash
cd /Users/aleksandr/Local/web-projects/poetry-site
docker-compose up
```

Open `http://localhost:8080`.

If you want to run the backend directly, use the same environment variables as Docker (`DATABASE_URL`, `UPLOADS_DIR`, `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`).

---

## Admin Usage

1. Open the site, click **Login** (top right).
2. Log in with credentials from `.env`.
3. Click **Admin** in the nav.

**Poems tab:**
- Add, edit, delete poems.
- Drafts are visible only to admins.
- Upload one image per poem (JPG/PNG, max 1MB).
- Version history keeps previous edits.
- **Export Poems** downloads a ZIP with poems, comments, and images.
- **Import Poems** imports a ZIP with poems, comments, and images.

**About Page tab:** Edit your name, bio, and photo URL.

**Comments tab:** Review and delete comments.

**Password tab:** Change admin password.

---

## API Reference (Selected)

All admin endpoints require `Authorization: Bearer <token>`.

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

Interactive docs: `/api/docs` and `/api/redoc`.

---

## Documentation

- Start here: `documentation/INDEX.md`
- i18n: `documentation/I18N_GUIDE.md`
- Add language: `documentation/ADD_NEW_LANGUAGE.md`
- Testing: `documentation/TESTING_GUIDE.md`
- Export/import: `documentation/EXPORT_IMPORT_GUIDE.md`
