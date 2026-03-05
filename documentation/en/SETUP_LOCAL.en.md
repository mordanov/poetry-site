# Local Setup — Poetry Site

## Requirements
- Docker + Docker Compose
- macOS, Linux, or Windows with Docker Desktop

## Run with Docker Compose
```bash
cd /Users/aleksandr/Local/poetry-site
docker-compose up
```
Open `http://localhost`.

## Environment variables
Copy `.env.example` to `.env` and set:
- `SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- Optional: `DB_PATH`, `UPLOADS_DIR`

## Common issues
- **Port 80 in use**: change ports in `docker-compose.yml` to `8080:80` and open `http://localhost:8080`.
- **Stale data**: `docker-compose down -v` then `docker-compose up`.
- **Cached frontend**: hard refresh or clear cache.

## Useful links
- `documentation/QUICK_COMMANDS.en.md`
- `documentation/TESTING_GUIDE.en.md`

**Русская версия:** `SETUP_LOCAL.md`

*Last updated: February 28, 2026*

