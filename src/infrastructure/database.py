import sqlite3
import pandas as pd
import os

DB_PATH = "data/league_data.db"

def save_to_db(df: pd.DataFrame, table_name: str):
    # Make sure that 'data/' folder exists.
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def read_from_db(query: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, conn)
    conn.close()
    return df