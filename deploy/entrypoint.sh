#!/bin/sh
set -e

# Wait for DB (basic) - try a few times
tries=0
max_tries=10
until python manage.py migrate --noinput 2>/dev/null || [ "$tries" -ge "$max_tries" ]; do
	tries=$((tries + 1))
	echo "Waiting for database... ($tries/$max_tries)"
	sleep 2
done

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3 --log-level info
