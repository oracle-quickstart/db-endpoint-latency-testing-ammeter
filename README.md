# DELTA - FastAPI based WebApp to Test Database Latency (NEW, 2025)

This project is a secure, lightweight SaaS-like database latency testing tool with a Mobile GUI, along with REST API.



https://github.com/user-attachments/assets/74497e35-a85b-4051-bee0-99a3c1ed67d0



Built with ❤️ using FastAPI.  


## 1. Clone Repository ##
```bash
git clone https://github.com/oracle-quickstart/db-endpoint-latency-testing-ammeter.git && cd db-endpoint-latency-testing-ammeter/
```

## 2. Set `APP_ADMIN_PASS` environment variable ##
```bash
export APP_ADMIN_PASS='abcd1234'
```

## 3. Quick Build with One-Command ##
```bash
 bash build.sh
```

## 4. Launch the Web App; Only required when you restart the App ##
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
## 5. Open the DB Latency app in our browser ##
```
https://localhost:8000
```
- Log in: `admin` / `abcd1234` (update with your password which you set for `APP_ADMIN_PASS` environment variable).
- Fill out the form and run latency tests in real time with live chart and table views.
- For any errors (connection, authentication) you'll see detailed front-end feedback.
  
<img width="655" alt="Screenshot 2025-07-04 at 2 49 25 AM" src="https://github.com/user-attachments/assets/c15b53dc-e138-4448-9777-e980db4354f0" />


## 6. Default SQL : API Usage via Curl/CLI MySQL Example ##
```bash
curl -u admin:abcd1234 -X POST https://localhost:8000/api/test-latency \
  -k \
  -d dbtype=mysql \
  -d host=localhost \
  -d port=3390 \
  -d username=snare \
  -d password="abcdABCD1234##" \
  -d database=snarepoc \
  -d interval=1 \
  -d period=10 \
  | jq .
```



## 7. Custom User SQL : API Usage via Curl/CLI MySQL Example ##

To test with a custom SQL query from the command line, simply add a -d custom_sql="YOUR SQL HERE" parameter to your curl command, like this:

```bash
curl -u admin:abcd1234 -X POST https://localhost:8000/api/test-latency \
  -k \
  -d dbtype=mysql \
  -d host=localhost \
  -d port=3390 \
  -d username=snare \
  -d password="abcdABCD1234##" \
  -d database=snarepoc \
  -d interval=1 \
  -d period=10 \
  -d custom_sql="select count(*) from WIN2019SNAREDC_SNARE_IA;" \
  | jq .
```

- If `custom_sql` is included (and not empty), that query is used for measuring latency (instead of `SELECT 1`).

- All other parameters stay the same as before.

- You can enter multi-line SQL in the terminal by wrapping it in quotes, or you can pipe in a file with `-d custom_sql="$(cat myquery.sql)"`.

### Important Note when using Custom queries ###
- Custom queries that are slower will always yield fewer completed test cycles in a fixed period. For eg: If your custom query takes, for example, 0.3 seconds and your interval is 1 second, each full cycle is actually ~1.3s, so over a 10 second period you’ll only get about 7-8 cycles.
  
- For `SELECT 1`, each loop is closer to 1s so you see 10 full cycles.
  
- This is expected behavior and the code is running safely/correctly.
  
- Custom queries that are slower will always yield fewer completed test cycles in a fixed period. Hence use Custom queries carefully.

##  🔌 Databases Supported

### 📌 Oracle DB  
- Amazon RDS Oracle
- OCI Autonomous Database
- OCI VMDB
- OCI Exadata Cloud Service
- Oracle Database On-Premise

### 📌 PostgreSQL
- Amazon RDS Postgres
- Amazon RDS Aurora Postgres
- Postgres On-premise 

### 📌 MySQL  
- Amazon RDS MySQL
- Amazon RDS Aurora MySQL
- OCI MySQL Database Service
- OCI MySQL Heatwave
- MySQL On-Premise

### 📌 URL - HTTPS | HTTP 
- Check Public or Private URLs for latency

## Contributing

This project welcomes contributions from the community. Before submitting a pull request, please [review our contribution guide](./CONTRIBUTING.md)

## Security

Please consult the [security guide](./SECURITY.md) for our responsible security vulnerability disclosure process

## License

Copyright (c) 2025 Oracle and/or its affiliates.

Released under the Apache License Version 2.0, January 2004
<http://www.apache.org/licenses/>.
