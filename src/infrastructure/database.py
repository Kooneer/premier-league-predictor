import sqlite3
import pandas as pd
import os
import sys

DB_PATH = "data/league_data.db"

def save_to_db(df: pd.DataFrame, table_name: str):
    try:
        # Make sure that 'data/' folder exists.
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Success: Data successfully saved to table '{table_name}'.")
    except sqlite3.Error as e:
        print(f"SQLite error during save'{table_name}': {e}", file=sys.stderr)
        raise e
    except Exception as e:
        print(f"Unexpected error during save: {e}", file=sys.stderr)
        raise e
    finally:
        if 'conn' in locals():
            conn.close()

def read_from_db(query: str) -> pd.DataFrame:
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(query, conn)
        return df
    except sqlite3.Error as e:
        print(f"SQLite error during execute query [{query}]: {e}", file=sys.stderr)
        return pd.DataFrame()
    except Exception as e:
        print(f"Unexpected error during read: {e}", file=sys.stderr)
        return pd.DataFrame()
    finally:
        if 'conn' in locals():
            conn.close()