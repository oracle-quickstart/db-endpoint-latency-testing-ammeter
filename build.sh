#!/bin/bash

README_URL="https://github.com/oracle-quickstart/db-endpoint-latency-testing-ammeter/blob/main/README.md"

set -e

echo "🔧 [1/5] Creating Python virtual environment (.venv)..."
if python3 -m venv .venv; then
    echo "✅ Virtual environment created."
else
    echo "❌ Failed to create venv. Please check your Python installation."
    echo "Refer to manual setup: $README_URL"
    exit 1
fi

echo "🔧 [2/5] Activating virtual environment..."
# shellcheck source=/dev/null
if source .venv/bin/activate 2>/dev/null; then
    echo "✅ Virtual environment activated."
else
    echo "❌ Failed to activate virtual environment."
    echo "Refer to manual setup: $README_URL"
    exit 1
fi

echo "🔧 [3/5] Installing requirements from requirements.txt..."
if pip install --upgrade pip > /dev/null 2>&1 && pip install -r requirements.txt; then
    echo "✅ Dependencies installed."
else
    echo "❌ Failed to install dependencies."
    echo "Refer to manual setup: $README_URL"
    exit 1
fi

echo "� [4/5] Generating self-signed SSL certificate if not present..."
SSL_DIR="ssl"
KEY_FILE="$SSL_DIR/key.pem"
CERT_FILE="$SSL_DIR/cert.pem"

if ! command -v openssl &> /dev/null; then
  echo "❌ OpenSSL is required for SSL certificate generation but is not installed."
  echo "Refer to manual setup: $README_URL"
  exit 1
fi

mkdir -p "$SSL_DIR"
if [[ -f "$KEY_FILE" && -f "$CERT_FILE" ]]; then
    echo "✅ SSL certificate and key found."
else
    echo "Generating self-signed cert/key. Expect prompts for certificate info."
    openssl req -x509 -nodes -days 825 -newkey rsa:2048 \
      -keyout "$KEY_FILE" -out "$CERT_FILE" \
      -subj "/C=US/ST=Self/L=Self/O=Self/CN=localhost"
    if [[ $? -eq 0 ]]; then
        echo "✅ SSL certificate generated."
    else
        echo "❌ Failed to generate SSL certificate."
        echo "Refer to manual setup: $README_URL"
        exit 1
    fi
fi

echo "🚦 [5/5] Launching app with uvicorn (https://localhost:8000, self-signed SSL)..."
if uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile "$KEY_FILE" --ssl-certfile "$CERT_FILE"; then
    echo "✅ App launched with HTTPS."
else
    echo "❌ Failed to launch the app. Please check above for errors."
    echo "Refer to manual setup: $README_URL"
    exit 1
fi
