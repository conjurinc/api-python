FROM conjurinc/api-python

RUN apt-get update -y && apt-get install -y python-dev libpq-dev curl vim postgresql-client

RUN mkdir -p /src
WORKDIR /src

COPY requirements* .
RUN pip install -r requirements.txt

ADD . .

ENV PYTHONPATH /app:/src
