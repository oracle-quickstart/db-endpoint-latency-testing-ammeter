import time
import datetime
import numpy as np
import requests

import oracledb
import psycopg2
import pymysql

# Optionally, handle MS SQL if needed
try:
    import pyodbc
    mssql_ok = True
except ImportError:
    mssql_ok = False

def run_latency_test(
    dbtype,
    host="",
    port="",
    username="",
    password="",
    database="",
    url="",
    interval=1.0,
    period=10
):
    query_times = []
    result_info = {"success": False, "error": None, "latency_stats": {}, "details": []}
    try:
        end_time = time.perf_counter() + period
        while time.perf_counter() < end_time:
            t0 = time.perf_counter()
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                if dbtype == "oracle":
                    conn = oracledb.connect(user=username, password=password, dsn=host)
                    cursor = conn.cursor()
                    cursor.execute("select 1 from dual")
                    cursor.fetchall()
                    cursor.close()
                    conn.close()
                elif dbtype == "postgresql":
                    conn = psycopg2.connect(host=host, port=port, dbname=database, user=username, password=password)
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
                    cursor.fetchall()
                    cursor.close()
                    conn.close()
                elif dbtype == "mysql":
                    conn = pymysql.connect(host=host, port=int(port), user=username, password=password, db=database)
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
                    cursor.fetchall()
                    cursor.close()
                    conn.close()
                elif dbtype == "sqlserver" and mssql_ok:
                    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={host},{port};DATABASE={database};UID={username};PWD={password}"
                    conn = pyodbc.connect(conn_str)
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
                    cursor.fetchall()
                    cursor.close()
                    conn.close()
                elif dbtype == "url":
                    response = requests.get(url)
                else:
                    raise Exception(f"Unsupported dbtype: {dbtype}")
                success = True
                error = None
            except Exception as ex:
                success = False
                error = str(ex)
            t1 = time.perf_counter()
            query_time = (t1 - t0) * 1000
            query_times.append(query_time)
            result_info["details"].append({
                "timestamp": ts,
                "latency_ms": query_time,
                "success": success,
                "error": error
            })
            time.sleep(interval)
        # Compute p99, p90, avg, stddev, mean on all query_times
        arr = np.array(query_times)
        result_info["latency_stats"] = {
            "p99": float(np.percentile(arr, 99)) if len(arr) else None,
            "p90": float(np.percentile(arr, 90)) if len(arr) else None,
            "avg": float(np.mean(arr)) if len(arr) else None,
            "stddev": float(np.std(arr)) if len(arr) else None,
            "mean": float(np.mean(arr)) if len(arr) else None,
            "runs": len(arr),
        }
        result_info["success"] = all(x["success"] for x in result_info["details"])
        result_info["error"] = next((x["error"] for x in result_info["details"] if x["error"]), None)
    except Exception as ex:
        result_info["success"] = False
        result_info["error"] = str(ex)
    return result_info
