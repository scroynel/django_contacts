#!/bin/sh

# Stop on any error
set -e

# A function to wait for the database (so that Django doesn't crash on startup)
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting PostgreSQL..."
    # Check the availability of the database port (usually 5432)
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL запущен!"
fi

echo "--> Applying migrations..."
python manage.py migrate --noinput

echo "--> Setting up initial data..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
from contacts.models import ContactStatusChoices

# 1. Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
    print('✅ Superuser created')

# 2. Basic statuses (name, code)
statuses = [
    ('Nowy', 'new'),
    ('W Trakcie', 'in_progress'),
    ('Zagubiony', 'lost'),
    ('Nieaktualny', 'outdated')
]

for name, code in statuses:
    obj, created = ContactStatusChoices.objects.get_or_create(
        name=name,
        code=code 
    )
    if created:
        print(f'✅ Status "{name}" (код: {code}) added')
    else:
        # If we have status we can update it
        if obj.name != name:
            obj.name = name
            obj.save()
            print(f'🔄 Status name with code "{code}" updated on "{name}"')
EOF
# hand over control to the main (runserver)
exec "$@"