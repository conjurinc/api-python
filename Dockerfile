FROM python:2.7-slim

RUN mkdir -p /app
WORKDIR /app

COPY requirements* /app/
RUN pip install -r requirements.txt -r requirements_dev.txt

VOLUME /app
VOLUME /artifacts
