# DELTA - Database Latency Checker Tool (NEW, 2025)

This project is a next-generation database endpoint latency benchmarking tool, purpose-built for modern hybrid cloud and distributed application architecture. Its unique value comes from its ability to precisely measure, visualize, and diagnose both network round-trip latency and SQL execution time for a wide range of databases—including Oracle (on-prem and Autonomous/ADB), PostgreSQL, MySQL, and even HTTP/HTTPS endpoints. 

By running YOUR own query, this tool captures every millisecond: DNS, handshake, connection pool, DB engine, result marshaling—just as your app user sees it. This is true end-to-end, *application-perceived* latency and not just network latency.


__Key Features:__

- __Granular Latency Breakdown:__ For every test, the tool separately measures the network connect time and the server-side SQL execution time. This allows you to see whether delays come from raw network/infrastructure, from database query planning/execution, or both.
- __End-to-End and Per-Operation Metrics:__ Outputs both total and component latencies for each query iteration, viewable in tables and visualized in real-time charts.
- __Live, Interactive UI:__ Includes a mobile-friendly GUI for interactive testing, as well as a full REST API for automation and integration with CI/CD or monitoring workflows.
- __Cloud & Hybrid-Ready:__ Designed for real-world topologies, it works with databases anywhere—public cloud (AWS, OCI, GCP, Azure), private datacenters, or in hybrid scenarios.
- __Easy Secure Remote Testing:__ Supports SSH tunnels so you can safely benchmark against remote cloud VMs or databases not directly exposed to the public internet.
- __Flexible Connection Patterns:__ Accepts detailed connection parameters or industry-standard DSN strings, supporting advanced Oracle topologies and features like TCPS (TLS) secure connections and failover.
- __Custom SQL Query Support:__ Test both trivial connectivity and the performance/latency of real, business-relevant workload queries.
- __Cross-Database Comparison:__ Enables performance comparisons across database types and clouds, supporting architectural and vendor selection.
- __Open, Extensible, and Developer-Friendly:__ FastAPI/REST backend, Python client code for scripting, and a well-documented interface for extension to additional DB engines or metrics.

__How It Helps:__ 

This tool equips architects, SREs, DBAs, and developers to:

- Quantify and visualize the real impact of hybrid or multi-cloud designs, by showing where latency is introduced in split-architecture applications.
- Simulate user experience for apps where the app and database reside in different data centers, clouds, or geographies.
- Optimize architecture design and deployment decisions by differentiating between network-related and DB-query-related bottlenecks.
- Validate and baseline connectivity, driver, TLS, and authentication configurations for complex, regulated, or highly available environments.
- Inform SLAs and help justify needed investments in network or database tuning.


## DELTA - Database Endpoint Latency Testing Ammeter
![image](https://github.com/user-attachments/assets/2fbb6927-0f48-4a85-9ae6-74efb63e6ef0)


https://github.com/user-attachments/assets/1fdf1e00-21bc-4be2-9815-a253a64df796

Built with ❤️ using FastAPI.  

##  🔌 Databases Supported

### 📌 Oracle DB  
- Amazon RDS for Oracle
- OCI Autonomous Database (without Wallet TLS)
- OCI Base Database Service
- OCI Exadata Cloud Service - Dedicated
- OCI Exascale Service- Dedicated
- Oracle Database@Azure
- Oracle Database@GCP
- Oracle Database@AWS
- Oracle Database installed on OnPremises or on any other cloud provider in a VM

### 📌 PostgreSQL
- Amazon RDS Postgres
- Amazon RDS Aurora Postgres
- OCI PostgreSQL
- PostgreSQL installed on OnPremises or on any other cloud provider in a VM

### 📌 MySQL  
- Amazon RDS MySQL
- Amazon RDS Aurora MySQL
- Heatwave@AWS
- OCI MySQL Heatwave
- MySQL installed on OnPremises or on any other cloud provider in a VM

### 📌 URL - HTTPS | HTTP 
- Check Public or Private URLs for latency

## Pre-Requisites ##

`Python >=3.9`

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
## 4. Open the DB Latency app in our browser ##
```
https://localhost:8000
```
- Log in: `admin` / `abcd1234` (update with your password which you set for `APP_ADMIN_PASS` environment variable).
- Fill out the form and run latency tests in real time with live chart and table views.
- For any errors (connection, authentication) you'll see detailed front-end feedback.
  
<img width="655" alt="Screenshot 2025-07-04 at 2 49 25 AM" src="https://github.com/user-attachments/assets/c15b53dc-e138-4448-9777-e980db4354f0" />


## 5. Default SQL : API Usage via Curl/CLI MySQL Example ##
```bash
curl -u admin:abcd1234 -X POST https://localhost:8000/api/test-latency \
  -k \
  -d dbtype=mysql \
  -d host=localhost \
  -d port=3390 \
  -d username=snare \
  -d password="" \
  -d database=snarepoc \
  -d interval=1 \
  -d period=10 \
  | jq .
```
## 6. Custom User SQL : API Usage via Curl/CLI MySQL Example ##

To test with a custom SQL query from the command line, simply add a -d custom_sql="YOUR SQL HERE" parameter to your curl command, like this:

```bash
curl -u admin:abcd1234 -X POST https://localhost:8000/api/test-latency \
  -k \
  -d dbtype=mysql \
  -d host=localhost \
  -d port=3390 \
  -d username=snare \
  -d password="" \
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


## 7. Stop and Start Shell Scripts (Linux and macOS) ##

- `start.sh`: Activates the Python virtual environment and launches uvicorn with HTTPS, using the generated self-signed certificate.
- `stop.sh`: Finds and terminates any uvicorn process running your app cleanly and safely.

Stop the Delta App
```bash
bash stop.sh
```
Start the Delta App
```bash
bash start.sh
```

---

# Testing Remote Databases Over SSH Tunnel and API

This section shows how to set up SSH tunnels to connect to remote databases from your local machine, and how to test each supported database type using the REST API or the GUI.

## SSH Tunnel Setup

### Oracle Autonomous Database (ADB) SSH Tunnel
```bash
ssh -fNT -v -L 1522:10.180.2.238:1521 opc@168.x.x.x -i "mydemo_vcn.priv"
```
### Local Oracle DB SSH Tunnel
```bash
ssh -fNT -v -L 1521:10.180.2.158:1521 opc@168.x.x.x -i "mydemo_vcn.priv"
```
### PostgreSQL SSH Tunnel
```bash
ssh -fNT -v -L 5432:10.180.2.205:5432 opc@168.x.x.x -i "mydemo_vcn.priv"
```
### MySQL SSH Tunnel
```bash
ssh -fNT -v -L 3306:10.180.2.30:3306 opc@168.x.x.x -i "mydemo_vcn.priv"
```
## API Usage Examples

### 1. PostgreSQL

#### CLI
```bash
curl -u admin:abcd1234 -X POST https://localhost:8000/api/test-latency \
  -k \
  -d dbtype=postgresql \
  -d host=localhost \
  -d port=5432 \
  -d username=ggadmin \
  -d password="" \
  -d database=dvdrental \
  -d interval=1 \
  -d period=5 \
  | jq .
```
#### GUI
<img width="458" alt="Screenshot 2025-07-05 at 11 02 13 PM" src="https://github.com/user-attachments/assets/528fe2d5-6f2f-45bd-bcf6-7ee1309fc51e" />


---

### 2. MySQL

#### CLI
```bash
curl -u admin:abcd1234 -X POST https://localhost:8000/api/test-latency \
  -k \
  -d dbtype=mysql \
  -d host=localhost \
  -d port=3306 \
  -d username=admin \
  -d password="" \
  -d database=dvdrental \
  -d interval=1 \
  -d period=5 \
  | jq .
```
#### GUI
<img width="458" alt="Screenshot 2025-07-05 at 11 02 20 PM" src="https://github.com/user-attachments/assets/d8895bcf-617c-447a-86d5-9ec65dba7476" />


---

### 3. Oracle (Standard/On-Premise)

#### CLI
```bash
curl -u admin:abcd1234 -X POST https://localhost:8000/api/test-latency \
  -k \
  -d dbtype=oracle \
  -d host=localhost \
  -d port=1521 \
  -d username=mpos \
  -d password="" \
  -d database=T1DB04 \
  -d interval=1 \
  -d period=5 \
  | jq .
```
#### GUI
<img width="376" alt="Screenshot 2025-07-05 at 11 42 13 PM" src="https://github.com/user-attachments/assets/880f58f8-3e09-40f1-9282-43341c7227a1" />

- If both "port" and "database" (service_name) are provided in the form/API, it constructs a ConnectParams object using host, port (as int), and service_name, then calls oracledb.connect(user, password, params=ConnectParams(...)).

- Otherwise, it falls back to oracledb.connect(user, password, dsn=host), allowing users to provide a complete DSN string in the "host" field.


---

### 4. Oracle ADB (TLS/TCPS Connection)

#### CLI
```bash
curl -u admin:abcd1234 -X POST https://localhost:8000/api/test-latency \
  -k \
  -d dbtype=oracle \
  -d host="(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=localhost))(connect_data=(service_name=****_s***_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=no)))" \
  -d username=dvdrental \
  -d password="" \
  -d interval=1 \
  -d period=5 \
  | jq .
```
#### GUI
<img width="376" alt="Screenshot 2025-07-05 at 11 33 13 PM" src="https://github.com/user-attachments/assets/351897b5-2c8b-482b-8310-c6a0401d58d6" />

- If both "port" and "database" (service_name) are provided in the form/API, it constructs a ConnectParams object using host, port (as int), and service_name, then calls oracledb.connect(user, password, params=ConnectParams(...)).

- Otherwise, it falls back to oracledb.connect(user, password, dsn=host), allowing users to provide a complete DSN string in the "host" field.

---

### 5. URL (HTTP/HTTPS Endpoint)

#### CLI
```bash
curl -u admin:abcd1234 -X POST https://localhost:8000/api/test-latency \
  -k \
  -d dbtype=url \
  -d url="https://google.com" \
  -d interval=1 \
  -d period=5 \
  | jq .
```
#### GUI
<img width="458" alt="Screenshot 2025-07-05 at 11 03 00 PM" src="https://github.com/user-attachments/assets/d97ee854-b7ff-4ee6-af5f-7c1fe127a281" />


---

# Bonus
## Windows Build File (Beta: Not tested)

Yes, you must first download (clone or extract) the GitHub repo to your Windows machine.

__Instructions:__

1. __Download the Repository__

   - If you have Git installed:

     - Open Command Prompt or PowerShell.
     - Run:

    ```javascript
      git clone https://github.com/oracle-quickstart/db-endpoint-latency-testing-ammeter.git
      cd db-endpoint-latency-testing-ammeter
     ```
   - Or download the zip from the GitHub releases or code page, and extract all files to a folder.

2. __Run the Build Script__

   - In Command Prompt (NOT PowerShell), navigate to the project folder.
   - Run:

  ```javascript
    build_windows.bat
   ```
   - This script will:

     - Create a virtual environment
     - Install dependencies
     - Generate a self-signed SSL certificate
     - Launch the app on [](https://localhost:8000)<https://localhost:8000>

__Requirements on Windows:__

- Python 3 (with pip)
- openssl.exe in PATH (commonly included with Git Bash or available at [slproweb.com](https://slproweb.com/products/Win32OpenSSL.html))

You do not need to manually install anything except Python and openssl; the script handles the rest.

## Contributing

This project welcomes contributions from the community. Before submitting a pull request, please [review our contribution guide](./CONTRIBUTING.md)

## Security

Please consult the [security guide](./SECURITY.md) for our responsible security vulnerability disclosure process

## License

Copyright (c) 2025 Oracle and/or its affiliates.

Released under the Apache License Version 2.0, January 2004
<http://www.apache.org/licenses/>.
