#!/bin/sh

echo "Waiting for PostgreSQL to start..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL started."

echo "Applying database migrations..."
python manage.py migrate

echo "Creating superuser if not exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
EOF

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000