import os
import secrets
from fastapi import FastAPI, Request, Form, status, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from . import dbtools

app = FastAPI(title="DB Endpoint Latency Tester", docs_url="/docs", redoc_url=None)

security = HTTPBasic()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

USERNAME = os.getenv("APP_ADMIN_USER", "admin")
PASSWORD = os.getenv("APP_ADMIN_PASS", None)

def sanitize_error(error):
    # Prevent detailed DB error/trace from leaking in API response
    if not error:
        return None
    return "Backend error. See server logs for details." if "Traceback" in error or "Exception" in error else error

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return credentials.username

@app.get("/", response_class=HTMLResponse)
def form(request: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "result": None})

@app.post("/test-latency", response_class=HTMLResponse)
def test_latency(
    request: Request,
    dbtype: str = Form(...),
    host: str = Form(""),
    port: str = Form(""),
    username: str = Form(""),
    password: str = Form(""),
    database: str = Form(""),
    url: str = Form(""),
    interval: float = Form(1.0),
    period: int = Form(10),
    custom_sql: str = Form(""),
    user: str = Depends(get_current_user)
):
    custom_sql = (custom_sql or "").strip()
    if custom_sql and len(custom_sql) > 5000:
        result = {
            "success": False,
            "error": "SQL query too long (limit 5000 chars)",
            "latency_stats": {}, "details": []
        }
        return templates.TemplateResponse("index.html", {
            "request": request,
            "user": user,
            "result": result,
            "dbtype": dbtype,
            "host": host,
            "port": port,
            "username": username,
            "database": database,
            "url": url,
            "interval": interval,
            "period": period,
            "custom_sql": custom_sql
        })
    result = dbtools.run_latency_test(
        dbtype=dbtype,
        host=host,
        port=port,
        username=username,
        password=password,
        database=database,
        url=url,
        interval=interval,
        period=period,
        custom_sql=custom_sql
    )
    # Sanitize error for UI as well
    if not result.get("success") and result.get("error"):
        result["error"] = sanitize_error(result["error"])
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user,
        "result": result,
        "dbtype": dbtype,
        "host": host,
        "port": port,
        "username": username,
        "database": database,
        "url": url,
        "interval": interval,
        "period": period,
        "custom_sql": custom_sql
    })

@app.post("/api/test-latency")
def api_test_latency(
    dbtype: str = Form(...),
    host: str = Form(""),
    port: str = Form(""),
    username: str = Form(""),
    password: str = Form(""),
    database: str = Form(""),
    url: str = Form(""),
    interval: float = Form(1.0),
    period: int = Form(10),
    custom_sql: str = Form(""),
    credentials: HTTPBasicCredentials = Depends(security)
):
    get_current_user(credentials)
    custom_sql = (custom_sql or "").strip()
    if custom_sql and len(custom_sql) > 5000:
        return JSONResponse({"success": False, "error": "SQL query too long (limit 5000 chars)"})
    try:
        result = dbtools.run_latency_test(
            dbtype=dbtype,
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
            url=url,
            interval=interval,
            period=period,
            custom_sql=custom_sql
        )
        # Sanitize error
        if not result.get("success") and result.get("error"):
            result["error"] = sanitize_error(result["error"])
        return JSONResponse(result)
    except Exception as e:
        # Never leak stack trace
        return JSONResponse({"success": False, "error": "Internal error. See server logs."})
