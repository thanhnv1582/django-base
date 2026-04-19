#!/bin/bash
# Docker entrypoint script
# Waits for dependencies, runs migrations, then starts the app

set -e

echo "─── Waiting for PostgreSQL... ───"
./docker/scripts/wait-for-it.sh "${DB_HOST:-postgres}:${DB_PORT:-5432}" --timeout=60 --strict -- echo "PostgreSQL ready."

echo "─── Waiting for Redis... ───"
./docker/scripts/wait-for-it.sh "${REDIS_HOST:-redis}:6379" --timeout=30 --strict -- echo "Redis ready."

echo "─── Running migrations... ───"
python manage.py migrate --noinput

echo "─── Collecting static files... ───"
python manage.py collectstatic --noinput --clear

echo "─── Starting application... ───"
exec "$@"
