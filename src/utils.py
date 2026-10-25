from pathlib import Path
import sqlite3, pandas as pd
ROOT=Path(__file__).resolve().parents[1]; DB_PATH=ROOT/"data/logitrack.db"
def get_connection(): return sqlite3.connect(DB_PATH,check_same_thread=False)
def initialize_database(force=False):
    conn=get_connection()
    for table in ["warehouses","drivers","vehicles","routes","shipments","deliveries","feedback"]:
        p=ROOT/"data/cleaned"/f"logitrack_{table}.csv"
        if not p.exists(): p=ROOT/"data/raw"/f"logitrack_{table}.csv"
        pd.read_csv(p).to_sql(table,conn,if_exists="replace",index=False)
    conn.close()
def query_df(sql): 
    with get_connection() as c: return pd.read_sql_query(sql,c)
