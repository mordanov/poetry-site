#!/bin/bash
cd /Users/aleksandr/Local/poetry-site
echo "=== Stopping containers ==="
docker-compose down
echo "=== Starting containers ==="
docker-compose up -d
echo "=== Waiting 5 seconds ==="
sleep 5
echo "=== Backend logs ==="
docker-compose logs backend | tail -50

