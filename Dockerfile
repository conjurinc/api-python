FROM ubuntu:14.04

RUN apt-get update -y && apt-get install -y python-pip

RUN mkdir -p /app
WORKDIR /app

COPY requirements* /app/
RUN pip install -r requirements.txt -r requirements_dev.txt

ADD . .

ENV PYTHONPATH /app
