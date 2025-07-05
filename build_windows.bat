@echo off
setlocal

set README_URL=https://github.com/oracle-quickstart/db-endpoint-latency-testing-ammeter/blob/main/README.md

echo [1/5] Creating Python virtual environment (.venv)...
if not exist .venv (
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create venv. Please check your Python installation.
        echo Refer to manual setup: %README_URL%
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

echo [2/5] Activating virtual environment...
call .venv\Scripts\activate
if errorlevel 1 (
    echo Failed to activate virtual environment.
    echo Refer to manual setup: %README_URL%
    exit /b 1
)

echo [3/5] Installing requirements from requirements.txt...
pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip.
    echo Refer to manual setup: %README_URL%
    exit /b 1
)
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    echo Refer to manual setup: %README_URL%
    exit /b 1
)

echo [4/5] Generating self-signed SSL certificate if not present...
set SSL_DIR=ssl
set KEY_FILE=%SSL_DIR%\key.pem
set CERT_FILE=%SSL_DIR%\cert.pem

if not exist %SSL_DIR% (
    mkdir %SSL_DIR%
)

if exist %KEY_FILE% if exist %CERT_FILE% (
    echo SSL certificate and key found.
) else (
    where openssl > nul 2>&1
    if errorlevel 1 (
        echo OpenSSL is required for SSL certificate generation but is not installed or not in PATH.
        echo Refer to manual setup: %README_URL%
        exit /b 1
    )
    openssl req -x509 -nodes -days 825 -newkey rsa:2048 ^
        -keyout %KEY_FILE% -out %CERT_FILE% ^
        -subj "/C=US/ST=Self/L=Self/O=Self/CN=localhost"
    if errorlevel 1 (
        echo Failed to generate SSL certificate.
        echo Refer to manual setup: %README_URL%
        exit /b 1
    )
)

echo [5/5] Launching app with uvicorn (https://localhost:8000, self-signed SSL)...
uvicorn app.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile "%KEY_FILE%" --ssl-certfile "%CERT_FILE%"
if errorlevel 1 (
    echo Failed to launch the app. Please check above for errors.
    echo Refer to manual setup: %README_URL%
    exit /b 1
)

endlocal
