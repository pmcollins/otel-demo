if [ "$1" = "--sdk" ]; then
  echo "got sdk flag"
  opentelemetry-instrument uvicorn main:app --port 8001
else
  echo "got NO sdk flag"
  opentelemetry-instrument uvicorn main:app --port 8001
fi
