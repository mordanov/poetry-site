# Poetry Site

Personal poetry site for a famous poet. Built with **FastAPI** backend, **Vanilla JS** SPA frontend, **PostgreSQL** database, served via **Nginx**, deployed with **Docker Compose**.

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
│       ├── poems.py         # CRUD + tags + export/import
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
│   ├── default.conf         # HTTP config (step 1)
│   └── default-https.conf   # HTTPS config (step 2, after cert)
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Local Development

### 1. Install backend dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Backend runs at http://localhost:8000  
API docs at http://localhost:8000/docs

### 2. Serve frontend locally

```bash
# From project root, serve static files
cd frontend
python -m http.server 3000
# Open http://localhost:3000/templates/index.html
```

Or just open `frontend/templates/index.html` in a browser, setting the API base to `http://localhost:8000` in `app.js`.

---

## Deployment on VPS

### Prerequisites
- VPS running Ubuntu 22.04 (1 vCPU / 1 GB RAM is enough)
- Docker + Docker Compose installed
- DNS record: `A www.yoursite.com → YOUR_VPS_IP` (also add `A yoursite.com → YOUR_VPS_IP`)
- Port 80 and 443 open in firewall

### Step 1 — Upload files

```bash
scp -r poetry-site/ user@YOUR_VPS_IP:~/
ssh user@YOUR_VPS_IP
cd ~/poetry-site
```

### Step 2 — Create .env

```bash
cp .env.example .env
nano .env
# Set SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD
```

Generate a secure secret key:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3 — Start with HTTP first (needed for cert)

```bash
docker compose up -d --build
```

Check it works at http://www.yoursite.com

### Step 4 — Get HTTPS certificate (Let's Encrypt, free)

```bash
docker compose run --rm certbot certonly \
  --webroot --webroot-path /var/www/certbot \
  -d www.yoursite.com -d yoursite.com \
  --email your@email.com --agree-tos --no-eff-email
```

### Step 5 — Switch to HTTPS config

```bash
cp nginx/default-https.conf nginx/default.conf
docker compose restart nginx
```

Your site is now live at https://www.yoursite.com 🎉

### Step 6 — Auto-renew certificate

Certbot renewal runs automatically via the certbot service in docker-compose.yml.
Add this to your crontab (`crontab -e`) to reload nginx when cert renews:

```
0 3 * * * docker compose -f ~/poetry-site/docker-compose.yml restart nginx
```

---

## Admin Usage

1. Go to https://www.yoursite.com, click **Login** (top right)
2. Log in with your credentials from `.env`
3. Click **Admin** in the nav

**Poems tab:** 
- Add, edit, delete poems. Each poem has title (optional), body, and tags.
- **Export Poems** (📥): Download all poems as JSON for backup or migration
- **Import Poems** (📤): Upload JSON file to bulk-import poems
- **Export Comments** (💬): Download all comments with poem info as JSON

**About Page tab:** Edit your name, bio text, and photo URL.

**Password tab:** Change your admin password.

> See [EXPORT_IMPORT_GUIDE.md](documentation/EXPORT_IMPORT_GUIDE.md) for detailed export/import usage.

---

## API Reference

All admin endpoints require `Authorization: Bearer <token>` header.

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/login` | — | Get JWT token |
| GET | `/api/auth/me` | ✓ | Current admin info |
| POST | `/api/auth/change-password` | ✓ | Change password |
| GET | `/api/poems` | — | List poems (optional `?tag=`) |
| GET | `/api/poems/tags` | — | List all tags with counts |
| GET | `/api/poems/{id}` | — | Get single poem |
| POST | `/api/poems` | ✓ | Create poem |
| PUT | `/api/poems/{id}` | ✓ | Update poem |
| DELETE | `/api/poems/{id}` | ✓ | Delete poem |
| GET | `/api/poems/export/all` | ✓ | Export all poems as JSON |
| POST | `/api/poems/import/all` | ✓ | Import poems from JSON |
| GET | `/api/poems/export/comments` | ✓ | Export all comments as JSON |
| GET | `/api/about` | — | Get about content |
| PUT | `/api/about` | ✓ | Update about content |
| GET | `/api/comments/{poem_id}` | — | Get comments for poem |
| POST | `/api/comments/{poem_id}` | — | Add comment |
| DELETE | `/api/comments/{id}` | ✓ | Delete comment |

Interactive docs available at `/api/docs` (development only).

---

## Backup

### Option 1: Export via Admin Panel (Recommended)
Use the built-in export feature in the admin panel:
- Click "📥 Export Poems" to download all poems as JSON
- Click "💬 Export Comments" to download all comments as JSON

This creates portable backup files that can be imported into any instance.

### Option 2: PostgreSQL Database Backup
Back up the entire database:

```bash
# Dump database to SQL file
docker compose exec db pg_dump -U ${POSTGRES_USER:-poetry_user} ${POSTGRES_DB:-poetry} > backup_$(date +%Y%m%d).sql

# Or backup using pg_dumpall for complete backup
docker compose exec db pg_dumpall -U ${POSTGRES_USER:-poetry_user} > backup_full_$(date +%Y%m%d).sql
```

Restore from backup:
```bash
docker compose exec -T db psql -U ${POSTGRES_USER:-poetry_user} -d ${POSTGRES_DB:-poetry} < backup_20260221.sql
```

### Option 3: Volume Backup
Copy the PostgreSQL data volume:
```bash
docker run --rm -v poetry-site_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data
```

---

## Migration

To migrate between instances:
1. Export poems and comments from old instance (Admin Panel)
2. Set up new instance with Docker Compose
3. Import poems using "📤 Import Poems" button
4. Comments are tied to poem IDs, so coordinate timing or manually adjust

---

## Upgrading to PostgreSQL

✅ **Already using PostgreSQL!** The site uses:
- PostgreSQL 16 Alpine
- SQLAlchemy ORM with asyncpg driver
- Connection pooling (20 base connections, 40 max overflow)
- Automatic connection recycling
