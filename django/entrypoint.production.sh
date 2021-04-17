#!/bin/sh
if [ "$DATABASE_NAME" = "postgres" ]
then
    echo "Waiting for postgres..."
    
    while ! nc -z $DATABASE_HOST 5432; do
      sleep 0.1
    done
    
    echo "PostgreSQL started"
fi

python manage.py collectstatic --noinput --settings=bolsonaro_api.settings.production
python manage.py migrate --noinput

if [ "$POPULATE_DB" = "True" ]
then
    echo "Populating database..."

    python manage.py createactions
    python manage.py createquotes

    echo "Database successfully populated!"
fi

exec "$@"