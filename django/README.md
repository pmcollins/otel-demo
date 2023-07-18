# OTel Demo Django App

This directory contains a Django web app and commands to both produce and ingest telemetry. The goals of this
functionality are to:

1) Demonstrate auto and manual instrumentation
2) Provide a way for a user to browse telemetry that thas been ingested
3) Test and validate auto-instrumentation end-to-end

### Web Application

The Django web app consists of a page that sends requests to other services, and a page to display metrics that
have been ingested locally.

When sending requests from Django to other services, you may select an HTTP client library (one of requests, httplib,
or httpx) before sending the request, as these three client libraries are instrumented independently.

Location: `./desktop`

### Ingest Command

The ingest command is a gRPC application that listens for metrics and traces and writes metrics to the local db.

Location: `./desktop/management/commands/ingest.py`

### Query Command

The query command accepts a metric name and returns a count of how many metrics in the db match that name.

Location: `./desktop/management/commands/query.py`

### PrintTime Command

The print-time command just prints the current time every second.

Location: `./desktop/management/commands/print-time.py`

### Operation

There is no need to start the Django app independently as start.sh in the parent directory starts all services in this
repo, but, you may start Django functionality independently:

1) Start ingest: `./start.sh [--sdk]`
2) Start server: `./start_server.sh [--sdk]`
3) Navigate to http://127.0.0.1:8000/

Add `--sdk` to enable instrumentation, otherwise it's not explicitly enabled.
