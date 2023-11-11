#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Create directories for every variable with DIR in its name
for var in $(compgen -v | grep DIR); do
  mkdir -p ${!var}
done

# Start your application with Gunicorn on port 80
exec gunicorn -b :80 app:app