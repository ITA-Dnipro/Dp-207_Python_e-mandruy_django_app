#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input
celery -A django_app worker -B -l INFO --detach
cd services/statistics_app/celery_utils/ && celery -A celery_app worker -B -l INFO --detach
tail -f /dev/null