# GitHub Actions Deployment Guide

## Автоматический деплой на сервер

Этот гайд объясняет, как настроить автоматический деплой приложения на сервер через GitHub Actions.

## Предварительные условия

- ✅ SSH приватный ключ пользователя `poetry-site`
- ✅ Доступ к репозиторию на GitHub
- ✅ Сервер с IP: `195.133.196.85`
- ✅ Docker установлен на сервере

## Шаг 1: Подготовка сервера

### На сервере (195.133.196.85):

```bash
# Подключиться по SSH как poetry-site
ssh poetry-site@195.133.196.85

# Создать директорию для проекта
mkdir -p /poetry
cd /poetry

# Убедиться, что Docker запущен
docker ps
```

## Шаг 2: Добавить секреты в GitHub

Перейдите в: **Repository Settings → Secrets and variables → Actions**

Добавьте следующие секреты:

### `SSH_PRIVATE_KEY`
Скопируйте содержимое приватного SSH ключа (весь блок от `-----BEGIN OPENSSH PRIVATE KEY-----` до `-----END OPENSSH PRIVATE KEY-----`)

### `SERVER_HOST`
```
195.133.196.85
```

### `SERVER_USER`
```
poetry-site
```

## Как это работает

1. **Триггер**: При пуше в ветку `main` автоматически запускается workflow
2. **Чекаут кода**: GitHub Actions скачивает последнюю версию кода
3. **SSH подключение**: Подключается к серверу с помощью приватного ключа
4. **Клонирование/обновление**: Клонирует репо на сервер или делает git pull
5. **Docker**: Перестраивает и запускает контейнеры
6. **Проверка здоровья**: Проверяет, что API отвечает

## Просмотр логов деплоя

1. Перейдите на страницу репозитория
2. Нажмите на вкладку **Actions**
3. Найдите последний workflow run
4. Нажмите на него и посмотрите логи

## Логирование на сервере

Деплой логируется в Docker:

```bash
# Логи backend
docker-compose logs backend -f

# Логи всех сервисов
docker-compose logs -f

# Статус контейнеров
docker-compose ps
```

## Возможные проблемы

### SSH подключение не работает
- ✅ Проверьте, что приватный ключ правильно добавлен в секреты
- ✅ Убедитесь, что публичный ключ на сервере в `~/.ssh/authorized_keys`
- ✅ Проверьте права доступа: `chmod 600 ~/.ssh/authorized_keys`

### Docker команды не работают
- ✅ Убедитесь, что пользователь `poetry-site` в группе `docker`
  ```bash
  groups poetry-site
  # Если нет, добавьте:
  sudo usermod -aG docker poetry-site
  # Перезагрузитесь или выполните:
  newgrp docker
  ```

### Деплой зависает
- ✅ Проверьте место на диске: `df -h`
- ✅ Проверьте логи Docker: `docker-compose logs`

## Ручной деплой

Если нужно развернуть вручную на сервере:

```bash
ssh poetry-site@195.133.196.85
cd /poetry
git pull origin main
docker-compose down
docker-compose up -d --build
```

## Переменные окружения

Если нужны переменные окружения для приложения, они должны быть в:
- `.env` файл в корне проекта (используется Docker Compose)
- Или добавить их в workflow как `env:`

## Помощь и отладка

### Проверить SSH доступ вручную

```bash
ssh -i ~/.ssh/id_rsa poetry-site@195.133.196.85 "docker ps"
```

### Проверить репозиторий на сервере

```bash
ssh poetry-site@195.133.196.85
cd /poetry
git log --oneline -5
git status
```

### Проверить здоровье приложения

```bash
curl http://195.133.196.85/api/health
```

## Полезные команды

```bash
# Просмотр последнего деплоя
docker-compose logs backend --tail 50

# Перезагрузить контейнеры
docker-compose restart

# Удалить всё и начать заново
docker-compose down -v
docker-compose up -d --build

# Проверить логи nginx
docker-compose logs nginx --tail 50
```

---

**Дата создания**: 2026-02-21
**Автор**: GitHub Copilot
