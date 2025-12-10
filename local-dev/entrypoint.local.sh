#!/usr/bin/env bash

mkdir -p /app/static/global /app/media || true
chmod -R 777 /app/static /app/media || true
chown -R appuser:appuser /app/static /app/media || true

sudo chown -R $USER:$USER static media
sudo chmod -R 777 static media



rm -rf /app/static/* || true

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 project.wsgi:application