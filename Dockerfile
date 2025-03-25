FROM python:3.9-slim as base

WORKDIR /app

COPY requirements.txt /app/
COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
