#!/bin/sh
for dir in fastapi flask bottle django; do
  cd "$dir"
  ./start.sh > output.log 2>&1 &
  echo "started $dir"
  cd ..
done
cd django
./start_server.sh > output-django.log 2>&1 &
echo "started django"
cd ..
tail -f */output*.log
