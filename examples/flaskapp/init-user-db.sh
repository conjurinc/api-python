#!/bin/bash -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER petstore WITH PASSWORD 'w^kftUagHmF2Ahph';
    CREATE DATABASE petstore;
    GRANT ALL PRIVILEGES ON DATABASE petstore TO petstore;
EOSQL
