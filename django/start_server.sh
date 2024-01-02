#!/bin/sh
if [ "$1" = "--sdk" ]; then
  OTEL_SERVICE_NAME=django-o11y DEPLOYMENT_ENVIRONMENT=local OTEL_DEPLOYMENT_ENVIRONMENT=otel-local DJANGO_SETTINGS_MODULE=otel_demo.settings opentelemetry-instrument python manage.py runserver --noreload
else
  python manage.py runserver
fi
