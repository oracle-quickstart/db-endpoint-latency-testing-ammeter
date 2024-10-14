import warnings
import argparse
import datetime
import time
import csv
import os
import numpy as np
from cryptography import __version__ as cryptography_version
from urllib.parse import urlparse
import requests
#import matplotlib.pyplot as plt

import oracledb
import psycopg2
import pymysql

if cryptography_version < "3.4":
    warnings.filterwarnings("ignore", category=UserWarning, message=".*will be forbidden in the future.*")

query_times = []

# Oracle Database credentials
oracle_un = 'admin'
oracle_pw = 'your_password'
oracle_cs = '(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.uk-london-1.oraclecloud.com))(connect_data=(service_name=m783q0lhgfda8ox_demoadb_high.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))'

# PostgreSQL credentials
pgsql_un = 'postgres'
pgsql_pw = 'your_password'
pgsql_host = 'localhost'
pgsql_port = '5432'
pgsql_db = 'postgres'

# MySQL credentials
mysql_un = 'mysql'
mysql_pw = 'your_password'
mysql_host = 'localhost'
mysql_port = '3306'
mysql_db = 'mysql'


# URL for testing
test_url = 'https://www.google.com'

def calculate_p99_latency():
    if len(query_times) > 0:
        p99_latency = np.percentile(query_times, 99)
        p90_latency = np.percentile(query_times, 90)
        stddev_latency = np.std(query_times)
        avg_latency = np.average(query_times)
        mean_latency = np.mean(query_times)
        print("++++++++++++++++++++++")
        print("P99 Latency: {:.2f} ms".format(p99_latency))
        print("P90 Latency: {:.2f} ms".format(p90_latency))
        print("++++++++++++++++++++++++++++++++++++++")
        print("Standard Deviation Latency: {:.2f} ms".format(stddev_latency))
        print("++++++++++++++++++++++++++++++++++++++")
        print("Average Latency: {:.2f} ms".format(avg_latency))
        print("++++++++++++++++++++++")
        print("Mean Latency: {:.2f} ms".format(mean_latency))
        print("++++++++++++++++++++++")

    else:
        print("No queries were executed.")

def oracle_ping(interval, csvfile):
    
    conn = oracledb.connect(user=oracle_un, password=oracle_pw, dsn=oracle_cs)
    cursor = conn.cursor()
    cursor.execute("select sys_context('USERENV','SID'), sys_context('USERENV','INSTANCE') from dual")
    sid, instance = cursor.fetchone()

    t0 = time.perf_counter()
    cursor.execute("select 1 from dual")
    cursor.fetchall()
    t1 = time.perf_counter()

    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time, sid, instance])

    cursor.close()
    conn.close()



def postgresql_ping(interval, csvfile):
    conn = psycopg2.connect(host=pgsql_host, port=pgsql_port, dbname=pgsql_db, user=pgsql_un, password=pgsql_pw)

    cursor = conn.cursor()

    t0 = time.perf_counter()
    cursor.execute("SELECT 1")
    cursor.fetchall()
    t1 = time.perf_counter()

    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time])

    cursor.close()
    conn.close()



def mysql_ping(interval, csvfile):
    conn = pymysql.connect(host=mysql_host, port=int(mysql_port), user=mysql_un, password=mysql_pw, db=mysql_db)

    cursor = conn.cursor()

    t0 = time.perf_counter()
    cursor.execute("SELECT 1")
    cursor.fetchall()
    t1 = time.perf_counter()

    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time])

    cursor.close()
    conn.close()



def sql_server_ping(interval, csvfile):
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={sql_server_host},{sql_server_port};DATABASE={sql_server_db};UID={sql_server_un};PWD={sql_server_pw}'
    conn = pyodbc.connect(conn_str)

    cursor = conn.cursor()

    t0 = time.perf_counter()
    cursor.execute("SELECT 1")
    cursor.fetchall()
    t1 = time.perf_counter()

    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time])

    cursor.close()
    conn.close()



def url_ping(interval, csvfile):
    t0 = time.perf_counter()
    response = requests.get(test_url)
    t1 = time.perf_counter()

    # (The rest of the function remains the same)

    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time])



# cmd-line arguments
parser = argparse.ArgumentParser(description="Connect and run a query.")
parser.add_argument("--interval", type=float, help="interval between each query, default 1", default=1)
parser.add_argument("--period", type=int, help="runtime in seconds; default 60", default=60)
parser.add_argument("--csvoutput", help="write timings to the named CSV file")
parser.add_argument("--db", choices=['oracle', 'postgresql', 'mysql', 'sqlserver', 'url'], required=True, help="specify the database or url to test")
args = parser.parse_args()


if args.csvoutput is not None:
    csvfile = open(args.csvoutput, "w", newline="")
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "Query time (ms)", "SID", "Instance"])
else:
    csvfile = None


start_time = time.perf_counter()
end_time = start_time + args.period

# Main loop
while time.perf_counter() < end_time:
    if args.db == 'oracle':
        oracle_ping(args.interval, csvfile)
    elif args.db == 'postgresql':
        postgresql_ping(args.interval, csvfile)
    elif args.db == 'mysql':
        mysql_ping(args.interval, csvfile)
    elif args.db == 'sqlserver':
        sql_server_ping(args.interval, csvfile)
    elif args.db == 'url':
        url_ping(args.interval, csvfile)
    time.sleep(args.interval)

calculate_p99_latency()

# Plot the latencies on a graph
#plt.figure(figsize=(10, 5))
#plt.plot(query_times, marker='o')
#plt.title('Latency Over Time')
#plt.xlabel('Query Number')
#plt.ylabel('Latency (ms)')

# Save the plot to a file
#output_file = "latency_plot.png"
#plt.savefig(output_file, bbox_inches='tight', dpi=300)

# Display the plot
#plt.show()
