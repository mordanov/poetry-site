# Quick Commands — Poetry Site

## Start / Stop
```bash
cd /Users/aleksandr/Local/poetry-site
docker-compose up
docker-compose down
```

## Rebuild
```bash
docker-compose up --build
```

## Logs
```bash
docker-compose logs
docker-compose logs backend
docker-compose logs nginx
docker-compose logs -f
```

## Shell into containers
```bash
docker-compose exec backend bash
docker-compose exec nginx bash
```

## Health check
```bash
curl http://localhost/api/health
```

**Русская версия:** `QUICK_COMMANDS.md`

