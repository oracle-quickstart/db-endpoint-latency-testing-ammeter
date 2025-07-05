#!/bin/bash

SSL_DIR="ssl"
KEY_FILE="$SSL_DIR/key.pem"
CERT_FILE="$SSL_DIR/cert.pem"

if [[ ! -f ".venv/bin/activate" ]]; then
    echo "❌ Python virtual environment not found. Please run build.sh first."
    exit 1
fi

if [[ ! -f "$KEY_FILE" || ! -f "$CERT_FILE" ]]; then
    echo "❌ SSL certificate or key missing. Please run build.sh first."
    exit 1
fi

echo "🔑 Activating virtual environment..."
# shellcheck source=/dev/null
source .venv/bin/activate

echo "🚦 Starting uvicorn server with HTTPS (https://localhost:8000)"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile "$KEY_FILE" --ssl-certfile "$CERT_FILE"
