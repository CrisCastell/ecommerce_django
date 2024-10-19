FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY entrypoint.sh /app/
COPY entrypoint.sh /usr/local/bin/


ENTRYPOINT ["entrypoint.sh"]
CMD ["entrypoint.sh"]
