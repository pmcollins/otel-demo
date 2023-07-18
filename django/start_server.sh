#!/bin/sh
if [ "$1" = "--sdk" ]; then
  DJANGO_SETTINGS_MODULE=otel_demo.settings opentelemetry-instrument python manage.py runserver --noreload
else
  python manage.py runserver
fi
