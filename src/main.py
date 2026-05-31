import pandas as pd
from src.infrastructure.database import read_from_db, get_all_tables

def inspect_raw_data():
    print("Loading raw historical data for inspection...")
    
    table_name = "raw_historical_schedules" 
    df = read_from_db(f"SELECT * FROM {table_name}")
    
    if df.empty:
        print(f"Warning: Table '{table_name}' was not found or is empty.")
        print("Checking available tables in the database...")
        
        available_tables = get_all_tables()
        
        if available_tables:
            print(f"Available tables: {available_tables}")
            print("Please update 'table_name' variable with one of the names above.")
        else:
            print("The database is completely empty! Run 'python -m scripts.download_data' first.")
        return

    # --- DIAGNOSTIC REPORT ---
    print("\n" + "="*50)
    print("1. METADATA & COLUMN TYPES (df.info()):")
    print("="*50)
    print(df.info())
    # ... reszta raportu bez zmian ...
    
    print("\n" + "="*50)
    print("2. MISSING VALUES (NaN) PER COLUMN:")
    print("="*50)
    missing_data = df.isna().sum()
    print(missing_data[missing_data > 0] if missing_data.sum() > 0 else "No missing values found!")

    print("\n" + "="*50)
    print("3. DATA SAMPLE (FIRST 3 ROWS):")
    print("="*50)
    print(df.head(3))

if __name__ == "__main__":
    inspect_raw_data()