# DELTA - FastAPI based WebApp to Test Database Latency (NEW, 2025)

This project is a secure, lightweight SaaS-like database latency testing GUI and API, built with FastAPI.  

https://github.com/user-attachments/assets/e3eaf179-914b-4c17-bc47-35f17e86aee0


## Clone Repository ##
```bash
git clone https://github.com/oracle-quickstart/db-endpoint-latency-testing-ammeter.git && cd db-endpoint-latency-testing-ammeter/
```

## Quick Build with One-Command ##
```bash
 bash build.sh
```

## Alternate : Step-by-Step Manual Build ##

### 1. Create a Python Virtual Environment

```bash
python3 -m venv .venv
```

#### Activate on Unix/macOS:
```bash
source .venv/bin/activate
```

#### Activate on Windows:
```bash
.venv\Scripts\activate
```

### 2. Install requirements
```bash
pip3 install -r requirements.txt
```

### 3. Launch the Web App
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
### 4. Open your browser at:
```
http://localhost:8000
```
- Log in: `admin` / `change_this` (update password in `app/main.py` for production).
- Fill out the form and run latency tests in real time with live chart and table views.
- For any errors (connection, authentication) you'll see detailed front-end feedback.

![Screenshot 2025-07-03 at 11 25 54 PM](https://github.com/user-attachments/assets/1e26dd2c-9423-46b8-9a76-b05b689e72b6)

![Screenshot 2025-07-03 at 11 26 17 PM](https://github.com/user-attachments/assets/235f6251-3198-4cd4-99a7-63490b4f6405)

![Screenshot 2025-07-03 at 11 26 30 PM](https://github.com/user-attachments/assets/f1b17fb8-f637-4b86-95c9-52dd0b6e2067)

### 5. API Usage via Curl/CLI Example:
```bash
curl -u admin:change_this -X POST http://localhost:8000/api/test-latency -d dbtype=mysql -d host=localhost -d port=3390 -d username=testuser -d password="YOurP@ssword#12" -d database=testdb -d interval=1 -d period=10 | jq .
```
```

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1260  100  1145  100   115    107     10  0:00:11  0:00:10  0:00:01   259
{
  "success": true,
  "error": null,
  "latency_stats": {
    "p99": 65.00130997534143,
    "p90": 64.45847470022272,
    "avg": 59.44308740145061,
    "stddev": 3.661004661748353,
    "mean": 59.44308740145061,
    "runs": 10
  },
  "details": [
    {
      "timestamp": "2025-07-04 01:18:22",
      "latency_ms": 61.802583004464395,
      "success": true,
      "error": null
    },
    {
      "timestamp": "2025-07-04 01:18:23",
      "latency_ms": 61.06654200993944,
      "success": true,
      "error": null
    },
    {
      "timestamp": "2025-07-04 01:18:24",
      "latency_ms": 64.39145799959078,
      "success": true,
      "error": null
    },
    {
      "timestamp": "2025-07-04 01:18:25",
      "latency_ms": 53.58212499413639,
      "success": true,
      "error": null
    },
    {
      "timestamp": "2025-07-04 01:18:26",
      "latency_ms": 65.06162500591017,
      "success": true,
      "error": null
    },
    {
      "timestamp": "2025-07-04 01:18:27",
      "latency_ms": 57.83200000587385,
      "success": true,
      "error": null
    },
    {
      "timestamp": "2025-07-04 01:18:29",
      "latency_ms": 54.59125000925269,
      "success": true,
      "error": null
    },
    {
      "timestamp": "2025-07-04 01:18:30",
      "latency_ms": 57.854083002894185,
      "success": true,
      "error": null
    },
    {
      "timestamp": "2025-07-04 01:18:31",
      "latency_ms": 60.93537498963997,
      "success": true,
      "error": null
    },
    {
      "timestamp": "2025-07-04 01:18:32",
      "latency_ms": 57.31383299280424,
      "success": true,
      "error": null
    }
  ]
}
```

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
