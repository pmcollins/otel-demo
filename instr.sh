#!/bin/sh
for dir in django fastapi flask bottle; do
  cd "$dir"
  ./instr.sh --sdk > output.log 2>&1 &
  echo "started $dir"
  cd ..
done
cd django
./instr_server.sh --sdk > output-server.log 2>&1 &
echo "started django sever"
cd ..
