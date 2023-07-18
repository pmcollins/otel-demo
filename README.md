# OTel Demo

This directory contains several applications that can be used to both explore and test the generation of telemetry from
a variety of Python libaries. The libraries which are both used by these applications, and which are also supported by
OTel instrumentation, are the following: DB-API, sqlite3, gRPC, Bottle, Django, Fastapi, Flask, Pyramid, Tornado,
Httplib, Requests, and Httpx.

The primary application in this directory is Django (`./django`). The Django directory contains a web app as well as
a few commands (see the Django [README.md](django/README.md) for more info). The other
directories (`bottle`, `fastapi`, `flask`, `pyramid`, and `tornado`) contain skeletal applications using the framework
with the same name as the directory. These small applications just have a single endpoint each, and are are called by
the Django web app upon user request.

### Operation

To start all services, run `./start.sh`. This will cause seven services to start: `django/ingest`, `fastapi`, `flask`,
`bottle`, `pyramid`, `tornado`, and `django/runserver`. By default, these sevices send telemetry message to the
local backend, which by default are intercepted and handled by `django/ingest`.
