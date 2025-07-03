from fastapi import FastAPI, Request, Form, status, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from . import dbtools

app = FastAPI(title="DB Endpoint Latency Tester", docs_url="/docs", redoc_url=None)

security = HTTPBasic()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

USERNAME = "admin"
PASSWORD = "change_this"  # Set a strong secret in prod

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid credentials"})
    return credentials.username

@app.get("/", response_class=HTMLResponse)
def form(request: Request, user: str = Depends(get_current_user)):
    # No results on initial GET
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
    user: str = Depends(get_current_user)
):
    # All credentials are held transiently only for test run
    result = dbtools.run_latency_test(
        dbtype=dbtype,
        host=host,
        port=port,
        username=username,
        password=password,
        database=database,
        url=url,
        interval=interval,
        period=period
    )
    # Render index.html with results below
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
        "period": period
    })

@app.post("/api/test-latency")
def api_test_latency(
    dbtype: str,
    host: str = "",
    port: str = "",
    username: str = "",
    password: str = "",
    database: str = "",
    url: str = "",
    interval: float = 1.0,
    period: int = 10,
    credentials: HTTPBasicCredentials = Depends(security)
):
    # For API/CLI use -- returns result JSON
    get_current_user(credentials)
    result = dbtools.run_latency_test(
        dbtype=dbtype,
        host=host,
        port=port,
        username=username,
        password=password,
        database=database,
        url=url,
        interval=interval,
        period=period
    )
    return JSONResponse(result)
