FROM python:3.12

RUN apt-get update && apt-get install -y gcc libpq-dev

RUN pip install --no-cache-dir mlflow boto3 pymysql cryptography psycopg2

EXPOSE 5000

RUN mkdir -p /mlflow

WORKDIR /mlflow