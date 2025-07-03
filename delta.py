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
from getpass import getpass

#import matplotlib.pyplot as plt

import oracledb
import psycopg2
import pymysql

if cryptography_version < "3.4":
    warnings.filterwarnings("ignore", category=UserWarning, message=".*will be forbidden in the future.*")

query_times = []

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

def oracle_ping(interval, csvfile, user, password, dsn):
    conn = oracledb.connect(user=user, password=password, dsn=dsn)
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

def postgresql_ping(interval, csvfile, user, password, host, port, db):
    conn = psycopg2.connect(host=host, port=port, dbname=db, user=user, password=password)
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

def mysql_ping(interval, csvfile, user, password, host, port, db):
    conn = pymysql.connect(host=host, port=int(port), user=user, password=password, db=db)
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

def url_ping(interval, csvfile, url):
    t0 = time.perf_counter()
    response = requests.get(url)
    t1 = time.perf_counter()

    query_time = (t1 - t0) * 1000
    query_times.append(query_time)

    if csvfile is not None:
        writer = csv.writer(csvfile)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, query_time])

parser = argparse.ArgumentParser(description="Connect and run a query.")
parser.add_argument("--interval", type=float, help="interval between each query, default 1", default=1)
parser.add_argument("--period", type=int, help="runtime in seconds; default 60", default=60)
parser.add_argument("--csvoutput", help="write timings to the named CSV file")
parser.add_argument("--db", choices=['oracle', 'postgresql', 'mysql', 'url'], required=True, help="specify the database or url to test")
parser.add_argument("--user", help="Database username")
parser.add_argument("--password", help="Database password")
parser.add_argument("--host", help="Database host/DSN string")
parser.add_argument("--port", help="Database port")
parser.add_argument("--database", help="Database name")
parser.add_argument("--url", help="Test URL for latency")
args = parser.parse_args()

if args.csvoutput is not None:
    csvfile = open(args.csvoutput, "w", newline="")
    writer = csv.writer(csvfile)
    if args.db == "oracle":
        writer.writerow(["Timestamp", "Query time (ms)", "SID", "Instance"])
    else:
        writer.writerow(["Timestamp", "Query time (ms)"])
else:
    csvfile = None

start_time = time.perf_counter()
end_time = start_time + args.period

# Gather credentials if not provided
def prompt_if_none(val, prompt_text, secure=False):
    if val:
        return val
    if secure:
        return getpass(prompt_text)
    return input(prompt_text)

for _ in range(int(args.period // args.interval)):
    if args.db == 'oracle':
        user = prompt_if_none(args.user, "Oracle Username: ")
        password = prompt_if_none(args.password, "Oracle Password: ", secure=True)
        dsn = prompt_if_none(args.host, "Oracle DSN (connection string): ")
        oracle_ping(args.interval, csvfile, user, password, dsn)
    elif args.db == 'postgresql':
        user = prompt_if_none(args.user, "Postgres Username: ")
        password = prompt_if_none(args.password, "Postgres Password: ", secure=True)
        host = prompt_if_none(args.host, "Postgres Host: ")
        port = prompt_if_none(args.port, "Postgres Port: ")
        db = prompt_if_none(args.database, "Postgres DB Name: ")
        postgresql_ping(args.interval, csvfile, user, password, host, port, db)
    elif args.db == 'mysql':
        user = prompt_if_none(args.user, "MySQL Username: ")
        password = prompt_if_none(args.password, "MySQL Password: ", secure=True)
        host = prompt_if_none(args.host, "MySQL Host: ")
        port = prompt_if_none(args.port, "MySQL Port: ")
        db = prompt_if_none(args.database, "MySQL DB Name: ")
        mysql_ping(args.interval, csvfile, user, password, host, port, db)
    elif args.db == 'url':
        url = prompt_if_none(args.url, "Test URL: ")
        url_ping(args.interval, csvfile, url)
    time.sleep(args.interval)

calculate_p99_latency()
