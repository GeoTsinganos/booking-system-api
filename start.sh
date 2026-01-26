#!/usr/bin/env bash
set -euo pipefail
set -x

python --version
python manage.py migrate
python manage.py collectstatic --noinput
exec gunicorn booking_system.wsgi:application --bind 0.0.0.0:${PORT}
