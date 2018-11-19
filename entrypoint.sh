#!bin/sh
cd /ipt_connect

if [ "$DEV" == "true" ]; then
    python manage.py runserver 0.0.0.0:8000
    exit 1
fi

gunicorn --workers=${WORKERS} --bind=unix:/ipt_connect/ipt_connect.sock ipt_connect.wsgi