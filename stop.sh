#!/bin/bash

PID=$(ps aux | grep 'uvicorn app.main:app' | grep -v grep | awk '{print $2}')
if [ -z "$PID" ]; then
    echo "No uvicorn process found running app.main:app."
    exit 0
fi

echo "Stopping uvicorn process (PID $PID)..."
kill "$PID"
sleep 2
if ps -p $PID > /dev/null; then
    echo "uvicorn (PID $PID) did not stop, sending SIGKILL."
    kill -9 "$PID"
else
    echo "uvicorn stopped."
fi
