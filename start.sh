#!/bin/bash
set -e  # stop the script if any command fails

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Load environment variables from /vault/secrets/config file
export $(grep -v '^#' /vault/secrets/config | xargs)

# Load environment variables from /vault/secrets/mongodb-creds file
export $(grep -v '^#' /vault/secrets/mongodb-creds | xargs)

exec gunicorn -w 3 -b :80 app:app