#!/bin/sh

until cd /app
do
    echo "Waiting for daphne volume..."
done

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

daphne -b 0.0.0.0 -p 8001 clan.asgi:application
