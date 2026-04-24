#!/bin/bash
# Postgres init script — crea DB + user separati per LiteLLM e Langfuse
# Invocato automaticamente da postgres:15-alpine al primo avvio
# Vedi: https://hub.docker.com/_/postgres (sezione "Initialization scripts")

set -e
set -u

function create_user_and_database() {
    local database=$1
    local password=$2
    echo "  Creating user and database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE USER $database WITH PASSWORD '$password';
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $database;
        ALTER DATABASE $database OWNER TO $database;
EOSQL
}

if [ -n "${POSTGRES_MULTIPLE_DATABASES:-}" ]; then
    echo "Creating multiple databases: $POSTGRES_MULTIPLE_DATABASES"
    # Format: "db1:pw1,db2:pw2"
    for pair in $(echo "$POSTGRES_MULTIPLE_DATABASES" | tr ',' ' '); do
        db_name=$(echo "$pair" | cut -d: -f1)
        db_pw=$(echo "$pair" | cut -d: -f2)
        create_user_and_database "$db_name" "$db_pw"
    done
    echo "Multiple databases created"
fi
