# Local Setup — Poetry Site

## Requirements
- Docker + Docker Compose
- macOS, Linux, or Windows with Docker Desktop

## Run with Docker Compose
```bash
cd /Users/aleksandr/Local/web-projects/poetry-site
docker-compose up
```
Open `http://localhost:8080`.

## Environment variables
Copy `.env.example` to `.env` and set:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DATABASE_URL`
- `SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- Optional: `POET_NAME`, `UPLOADS_DIR`

## Common issues
- **Port 8080 in use**: change `POETRY_HTTP_PORT` in `.env`.
- **Stale data**: `docker-compose down -v` then `docker-compose up`.
- **Database not ready**: check `docker-compose logs db`.

## Useful links
- `documentation/en/QUICK_COMMANDS.en.md`
- `documentation/en/PROJECT_STRUCTURE.en.md`

**Русская версия:** `documentation/ru/SETUP_LOCAL.md`

*Last updated: March 18, 2026*
