# DB(D)  Endpoint(E)  Latency(L)  Testing(T)  Ammeter(A) 

## DELTA 

📌 Introducing DELTA (DB Endpoint Latency Testing Ammeter). DELTA is a tool to test real-world latency against a remote database using execution of a query and calculating the network return time. The tool provides functions to test latency of Oracle, MySQL and Postgres databases.

The tool uses the oracledb python package to connect to Oracle databases and execute a single query per request (you can specify multiple requests as well). The tool uses the time module to measure the time it takes to execute the query, fetch the results, and close the connection. It calculates the latency of each request and the average latency of all requests.


🔧 DELTA is a cloud tool to test real-world latency against a remote database endpoint using execution of a query and calculating the network return time. 


🔧 Network tools like ping ,iperf or tcp ping can only give you network based latency which does not always translate well to an application running those queries on a remote database. 


🐍 DELTA uses Python client for Oracle, MySQL and PostgreSQL to run a query like “SELECT 1” or "SELECT 1 FROM DUAL". You can then specific the number of executions of the query and DELTA calculates the average network round-trip time for all the executions of the query on the remote database. The script also includes error handling to track failed requests. You can also include your own custom queries. 



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


# Deploy

## Requirement

```
Python >= 3.6.8
```

## Clone Repo

```
git clone https://github.com/oracle-quickstart/db-endpoint-latency-testing-ammeter.git

cd db-endpoint-latency-testing-ammeter/
```

## Install Python packages
```
## On CentOS or Oracle Linux or Redhat Linux
sudo yum install postgresql postgresql-devel python36-devel

## On Ubuntu
sudo apt install libpq-dev python3.x-dev

## Install requirements
sudo pip3 install -r requirements.txt
```

# Calculate Latency for Oracle DB

Set the below credentials in the delta.py script
```
oracle_un='your_user'
oracle_pw='your_password'
oracle_cs='your_connection_string'
```
Run
```
python3 delta.py --db oracle --interval 3 --period 5 --csvoutput oracle_latency.csv
```


# Calculate Latency for MySQL 

Set the below credentials in the delta.py script
```
mysql_un = 'mysql'
mysql_pw = 'your_password'
mysql_host = 'localhost'
mysql_port = '3306'
mysql_db = 'mysql'
```
Run
```
python3 delta.py --db mysql --interval 3 --period 5 --csvoutput mysql_latency.csv
```

# Calculate Latency for PostgreSQL 

Set the below credentials in the delta.py script
```
pgsql_un = 'postgres'
pgsql_pw = 'your_password'
pgsql_host = 'localhost'
pgsql_port = '5432'
pgsql_db = 'postgres'
```
Run
```
python3 delta.py --db postgresql --interval 3 --period 5 --csvoutput postgres_latency.csv
```


# Calculate URL Latency 

Set the below parameter in the delta.py script
```
test_url = 'your_url'
```
Run
```
python3 delta.py --db url --interval 3 --period 5 --csvoutput url_latency.csv
```



# Test Cases for Each DB and URL

```
python3 delta.py --db oracle --interval 3 --period 5 --csvoutput oracle_latency.csv

python3 delta.py --db mysql --interval 3 --period 5 --csvoutput mysql_latency.csv

python3 delta.py --db postgresql --interval 3 --period 5 --csvoutput postgres_latency.csv

python3 delta.py --db url --interval 3 --period 5 --csvoutput url_latency.csv
```
