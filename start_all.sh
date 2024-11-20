#!/bin/sh
for dir in django fastapi flask bottle pyramid tornado; do
  cd "$dir"
  ./start.sh --sdk > output.log 2>&1 &
  echo "started $dir"
  cd ..
done
