# OTel Demo

This directory contains a Django web app and command to both produce and ingest telemetry. The goals of this
functionality are to:

1) demonstrate auto and manual instrumentation
2) provide a way for a user to browse telemetry that thas been ingested
3) test and validate auto-instrumentation end-to-end

It uses a variety of technologies that are currently supported by OTel Python auto-instrumentation: Django, DB-API,
sqlite3, and gRPC.

### Ingest

The ingest command is a gRPC application that listens for metrics and traces. At the time of writing, it
writes just metrics to the local db.

Location: `./management/commands/ingest.py`

### Web Application

The Django web app consists of one page that displays the raw metrics that have been ingested and written to the
db.

Location: `./desktop`

### Operation

1) Start ingest: run `python manage.py ingest`
2) Start the Django server: `./start_server_auto_instr.sh`
3) Navigate to http://127.0.0.1:8000/desktop/ to view metrics
