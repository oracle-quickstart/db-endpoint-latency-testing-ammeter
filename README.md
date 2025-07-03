# DELTA - FastAPI based WebApp to Test Database Latency (NEW, 2025)

This project is a secure, lightweight SaaS-like database latency testing GUI and API, built with FastAPI.  

![Screenshot 2025-07-03 at 11 25 54 PM](https://github.com/user-attachments/assets/1e26dd2c-9423-46b8-9a76-b05b689e72b6)

![Screenshot 2025-07-03 at 11 26 17 PM](https://github.com/user-attachments/assets/235f6251-3198-4cd4-99a7-63490b4f6405)

![Screenshot 2025-07-03 at 11 26 30 PM](https://github.com/user-attachments/assets/f1b17fb8-f637-4b86-95c9-52dd0b6e2067)

### 1. Clone Repository ###
```bash
git clone https://github.com/oracle-quickstart/db-endpoint-latency-testing-ammeter.git && cd db-endpoint-latency-testing-ammeter/
```

### 2. Create a Python Virtual Environment

```bash
python3 -m venv .venv

# Activate on Unix/macOS:
source .venv/bin/activate

# Activate on Windows:
.venv\Scripts\activate
```

### 3. Install requirements
```bash
pip3 install -r requirements.txt
```

### 4. Launch the Web App
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
### 5. Open your browser at:
```
http://localhost:8000
```
- Log in: `admin` / `change_this` (update password in `app/main.py` for production).
- Fill out the form and run latency tests in real time with live chart and table views.
- For any errors (connection, authentication) you'll see detailed front-end feedback.

### 6. API Usage via Curl/CLI Example:
```bash
curl -u admin:change_this -X POST http://localhost:8000/api/test-latency \
  -F dbtype=postgresql -F host=localhost -F port=5432 -F username=postgres -F password=yourpassword -F database=postgres -F interval=1 -F period=10
```
- API returns JSON, suitable for automation and CI.

---

## Command-Line (delta.py) Usage — Secure, No Stored Credentials

The original `delta.py` script remains available for CLI power users and can test Oracle, PostgreSQL, MySQL, and URLs. **No credentials are stored in this file**; you must supply all values as arguments or interactively via a prompt.


## Databases Supported 🔌 :

### Oracle DB >= 12.2 📌  : 
- Amazon RDS Oracle
- OCI Autonomous Database
- OCI VMDB
- OCI Exadata Cloud Service
- Oracle Database On-Premise

### Postgres >= 11 📌 :
- Amazon RDS Postgres
- Amazon RDS Aurora Postgres
- Postgres On-premise 

### MySQL >= 5.7 📌  : 
- Amazon RDS MySQL
- Amazon RDS Aurora MySQL
- OCI MySQL Database Service
- OCI MySQL Heatwave
- MySQL On-Premise

### URL - HTTPS | HTTP 📌 :
- Check Public or Private URLs for latency

## Contributing

This project welcomes contributions from the community. Before submitting a pull request, please [review our contribution guide](./CONTRIBUTING.md)

## Security

Please consult the [security guide](./SECURITY.md) for our responsible security vulnerability disclosure process

## License

Copyright (c) 2023 Oracle and/or its affiliates.

Released under the Apache License Version 2.0, January 2004
<http://www.apache.org/licenses/>.
