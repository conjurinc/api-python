FROM phusion/baseimage:0.9.16

# Install Python and pandoc
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip pandoc && \
  rm -rf /var/lib/apt/lists/*

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt -r requirements_dev.txt

VOLUME /artifacts
