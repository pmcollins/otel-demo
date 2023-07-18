if [ "$1" = "--sdk" ]; then
  opentelemetry-instrument uvicorn main:app --port 8001
else
  uvicorn main:app --port 8001
fi
