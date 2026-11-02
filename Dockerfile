FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PORT=5000
EXPOSE 5000

CMD gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 120
