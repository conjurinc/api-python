#!/bin/bash -e

docker-compose build

if [ ! -f data_key ]; then
  echo "Generating data key"
  docker-compose run --no-deps --rm possum data-key generate > data_key
fi

export POSSUM_DATA_KEY="$(cat data_key)"
export POSTGRES_PASSWORD="w^kftUagHmF2Ahph"

docker-compose up -d possumdb possum appdb

cat << "HEALTH" | docker-compose run --rm client bash
for i in $(seq 10); do
  curl -o /dev/null -fs -X OPTIONS http://possum > /dev/null && break
  echo -n "."
  sleep 2
done
HEALTH

echo Loading the database password into Possum
docker-compose run --rm client python load_secrets.py

docker-compose up -d app

docker-compose run --rm client
