if [ "$1" = "--sdk" ]; then
  opentelemetry-instrument python main.py
else
  python main.py
fi
