#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A clan worker --loglevel=info --concurrency 1 -E