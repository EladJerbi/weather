#!/bin/bash
set -e  # stop the script if any command fails

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Load environment variables from /vault/secrets/config file
export $(grep -v '^#' /vault/secrets/config | xargs)

# Create directories for every variable with DIR in its name
for var in $(compgen -v); do
  if [[ $var == *DIR ]]; then
    mkdir -p "${!var}"
  fi
done

exec gunicorn -w 3 -b :80 app:app