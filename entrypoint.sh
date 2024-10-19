#!/bin/sh
python manage.py migrate --noinput

python manage.py migrate --noinput


python manage.py loaddata fixtures/auth_fixtures.json fixtures/productos_fixtures.json


python manage.py collectstatic --noinput


exec gunicorn ecommerce_senzil.wsgi:application --bind 0.0.0.0:8000
