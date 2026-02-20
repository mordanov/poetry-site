# levgorev.com — Poetry Site

Personal poetry site for Lev Gorev. Built with **FastAPI** backend, **Vanilla JS** SPA frontend, **SQLite** database, served via **Nginx**, deployed with **Docker Compose**.

---

## Project Structure

```
poetry-site/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLite setup & migrations
│   ├── requirements.txt
│   ├── Dockerfile
│   └── routers/
│       ├── auth.py          # JWT login, password change
│       ├── poems.py         # CRUD + tags
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
- DNS record: `A www.levgorev.com → YOUR_VPS_IP` (also add `A levgorev.com → YOUR_VPS_IP`)
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

Check it works at http://www.levgorev.com

### Step 4 — Get HTTPS certificate (Let's Encrypt, free)

```bash
docker compose run --rm certbot certonly \
  --webroot --webroot-path /var/www/certbot \
  -d www.levgorev.com -d levgorev.com \
  --email your@email.com --agree-tos --no-eff-email
```

### Step 5 — Switch to HTTPS config

```bash
cp nginx/default-https.conf nginx/default.conf
docker compose restart nginx
```

Your site is now live at https://www.levgorev.com 🎉

### Step 6 — Auto-renew certificate

Certbot renewal runs automatically via the certbot service in docker-compose.yml.
Add this to your crontab (`crontab -e`) to reload nginx when cert renews:

```
0 3 * * * docker compose -f ~/poetry-site/docker-compose.yml restart nginx
```

---

## Admin Usage

1. Go to https://www.levgorev.com, click **Login** (top right)
2. Log in with your credentials from `.env`
3. Click **Admin** in the nav

**Poems tab:** Add, edit, delete poems. Each poem has title (optional), body, and tags.

**About Page tab:** Edit your name, bio text, and photo URL.

**Password tab:** Change your admin password.

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
| GET | `/api/about` | — | Get about content |
| PUT | `/api/about` | ✓ | Update about content |
| GET | `/api/comments/{poem_id}` | — | Get comments for poem |
| POST | `/api/comments/{poem_id}` | — | Add comment |
| DELETE | `/api/comments/{id}` | ✓ | Delete comment |

Interactive docs available at `/api/docs` (development only).

---

## Backup

Database is a single SQLite file. Back it up with:

```bash
docker compose exec backend sqlite3 /data/poetry.db .dump > backup_$(date +%Y%m%d).sql
```

Or copy the volume directly:
```bash
docker cp $(docker compose ps -q backend):/data/poetry.db ./backup.db
```

---

## Upgrading to PostgreSQL (later)

When the site grows, swap SQLite for PostgreSQL by:
1. Adding a `postgres` service to `docker-compose.yml`
2. Replacing `sqlite3` with `psycopg2` + `asyncpg` in `database.py`
3. Migrating data with `pg_restore`

The SQL schema is standard and fully compatible.
