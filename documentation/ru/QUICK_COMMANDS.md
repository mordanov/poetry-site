# ⚡ Быстрые команды для Poetry Site

## 🚀 Запуск

```bash
docker-compose up
docker-compose up -d
docker-compose up --build
```

## 🛑 Остановка

```bash
docker-compose down
docker-compose down -v
docker-compose restart
```

## 📊 Логи

```bash
docker-compose logs
docker-compose logs -f
docker-compose logs backend
docker-compose logs nginx
```

## 🔧 Контейнеры

```bash
docker-compose ps
docker-compose exec backend bash
docker-compose exec db psql -U ${POSTGRES_USER:-poetry_user} -d ${POSTGRES_DB:-poetry}
```

## 💾 PostgreSQL

```bash
# таблицы
\dt

# схема poems
\d poems

# количество стихов
docker-compose exec db psql -U ${POSTGRES_USER:-poetry_user} -d ${POSTGRES_DB:-poetry} -c "SELECT COUNT(*) FROM poems;"

# backup
docker-compose exec db pg_dump -U ${POSTGRES_USER:-poetry_user} ${POSTGRES_DB:-poetry} > poetry_backup_$(date +%Y%m%d).sql

# restore
docker-compose exec -T db psql -U ${POSTGRES_USER:-poetry_user} -d ${POSTGRES_DB:-poetry} < poetry_backup_20260318.sql

# health
docker-compose exec db pg_isready -U ${POSTGRES_USER:-poetry_user} -d ${POSTGRES_DB:-poetry}
```

## 🌐 API smoke

```bash
curl http://localhost/api/health
curl http://localhost/api/poems
curl http://localhost/api/about
```

## 🔐 Переменные окружения

```bash
docker-compose exec backend env | sort
docker-compose exec backend echo $DATABASE_URL
docker-compose exec backend echo $SECRET_KEY
```

## 🧹 Очистка

```bash
docker-compose down -v && docker system prune -a
docker volume rm poetry-site_postgres_data
```

## 🧪 Быстрая проверка

```bash
echo "=== STATUS ===" && docker-compose ps && \
echo "=== HEALTH ===" && curl -s http://localhost/api/health && echo
```
