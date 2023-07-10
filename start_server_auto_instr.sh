#!/bin/sh
DJANGO_SETTINGS_MODULE=otel_demo.settings opentelemetry-instrument python manage.py runserver --noreload
