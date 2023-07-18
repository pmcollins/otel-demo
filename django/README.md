# OTel Demo

This directory contains a Django web app and commands to both produce and ingest telemetry. The goals of this
functionality are to:

1) Demonstrate auto and manual instrumentation
2) Provide a way for a user to browse telemetry that thas been ingested
3) Test and validate auto-instrumentation end-to-end

It uses a variety of technologies that are currently supported by OTel Python auto-instrumentation: Django, DB-API,
sqlite3, and gRPC.

### Web Application

The Django web app consists of a single page that displays the raw metrics that have been ingested and written to the
db.

Location: `./desktop`  
Usage: `./start_server_auto_instr.sh` or `python manage.py runserver`

### Ingest

The ingest command is a gRPC application that listens for metrics and traces. At the time of writing, it
writes just metrics to the local db. It accepts an optional `--sdk` arg which sets up the OTel SDK and causes the
command to send telemetry to ingest.

Location: `./management/commands/ingest.py`  
Usage: `python manage.py ingest [--sdk]`

### Query

The query command accepts a metric name and returns a count of how many metrics in the db match that name. It accepts an
optional `--sdk` arg which sets up the OTel SDK and causes the command to send telemetry to ingest.

Location: `./management/commands/query.py`  
Usage: `python manage.py query some.metric [--sdk]`

### PrintTime

The print-time command just prints the current time every second. It accepts an optional `--sdk` arg which sets up the
OTel SDK and causes the command to send telemetry to ingest.

Location: `./management/commands/print-time.py`  
Usage: `python manage.py print-time [--sdk]`

### Operation

1) Start ingest (with instrumentation): `python manage.py ingest --sdk`
2) Start the Django server (with instrumentation): `./start_server_auto_instr.sh`
3) Navigate to http://127.0.0.1:8000/desktop/ to view metrics

![Screenshot 2023-07-11 at 2 34 30 PM](https://github.com/pmcollins/otel_demo/assets/141681/e004f9e8-b6a9-4bd2-a8c2-a239bc9a1100)
