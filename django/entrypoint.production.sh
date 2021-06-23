#!/bin/sh
python manage.py collectstatic --noinput --settings=bolsonaro_api.settings.production
python manage.py migrate --noinput
python manage.py create_actions
python manage.py create_quotes

cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='$ADMIN_USERNAME').exists():
    User.objects.create_superuser(username='$ADMIN_USERNAME', 
                                  email='$EMAIL_HOST_USER', 
                                  password='$ADMIN_PASSWORD')
    print("Superuser created!")
EOF

exec "$@"