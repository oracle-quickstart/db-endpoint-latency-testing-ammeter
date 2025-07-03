#!/bin/bash

README_URL="https://github.com/oracle-quickstart/db-endpoint-latency-testing-ammeter/blob/main/README.md"

set -e

echo "🔧 [1/4] Creating Python virtual environment (.venv)..."
if python3 -m venv .venv; then
    echo "✅ Virtual environment created."
else
    echo "❌ Failed to create venv. Please check your Python installation."
    echo "Refer to manual setup: $README_URL"
    exit 1
fi

echo "🔧 [2/4] Activating virtual environment..."
# shellcheck source=/dev/null
if source .venv/bin/activate 2>/dev/null; then
    echo "✅ Virtual environment activated."
else
    echo "❌ Failed to activate virtual environment."
    echo "Refer to manual setup: $README_URL"
    exit 1
fi

echo "🔧 [3/4] Installing requirements from requirements.txt..."
if pip install --upgrade pip > /dev/null 2>&1 && pip install -r requirements.txt; then
    echo "✅ Dependencies installed."
else
    echo "❌ Failed to install dependencies."
    echo "Refer to manual setup: $README_URL"
    exit 1
fi

echo "🚦 [4/4] Launching app with uvicorn (running at http://localhost:8000)..."
if uvicorn app.main:app --host 0.0.0.0 --port 8000
then
    echo "✅ App launched."
else
    echo "❌ Failed to launch the app. Please check above for errors."
    echo "Refer to manual setup: $README_URL"
    exit 1
fi
