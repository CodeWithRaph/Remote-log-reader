FROM python:3.14-alpine

WORKDIR /app

COPY . .

RUN apk add --no-cache \
    mariadb-connector-c-dev \
    gcc \
    musl-dev

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "./app_logs/run.py"]