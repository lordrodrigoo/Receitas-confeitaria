#!/usr/bin/env bash

# Apaga arquivos estáticos antes de coletar
rm -rf /app/static/* || true

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 project.wsgi:application