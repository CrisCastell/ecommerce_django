FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py loaddata fixtures/auth_fixtures.json fixtures/productos_fixtures.json && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]