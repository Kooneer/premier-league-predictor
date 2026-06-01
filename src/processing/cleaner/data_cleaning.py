import pandas as pd
import numpy as np
from src.infrastructure.database import read_from_db, get_all_tables

def inspect_table_data(table_name: str) -> None:
    """
    Inspect raw data from DB
    """
    print(f"Loading data from {table_name} for inspection...")
    
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
    
    print("\n" + "="*50)
    print("2. MISSING VALUES (NaN) PER COLUMN:")
    print("="*50)
    missing_data = df.isna().sum()
    print(missing_data[missing_data > 0] if missing_data.sum() > 0 else "No missing values found!")

    print("\n" + "="*50)
    print("3. DATA SAMPLE (FIRST 3 ROWS):")
    print("="*50)
    print(df.head(3))

def clean_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs initial data cleaning on raw historical Premier League schedules.
    Removes empty columns and parses dates/scores into ML-ready formats.
    """
    if df.empty:
        print("Warning: DataFrame is empty!")
        return df
    
    processed_df = df.copy()

    # Deleting 'notes' column cause it contains only empty values
    if 'notes' in processed_df:
        try: 
            processed_df = processed_df.drop(columns='notes')
        except Exception as e:
            print(f"Warning during drop 'notes': {e}")

    # Parsing 'date': "20:00 (21:00)" -> "20:00"; and save as datetime format
    if 'time' in processed_df:
        try:
            clean_time = processed_df['time'].str.split(' ').str[0]
            clean_date = processed_df['date'].str.split(' ').str[0]
            processed_df['datetime'] = pd.to_datetime(
                clean_date + ' ' + clean_time,
                errors='coerce',
                format='%Y-%m-%d %H:%M'
            )
            errors_counter = processed_df['datetime'].isnull().sum()
            if errors_counter > 0:
                print(f"Warning: There's {errors_counter} rows with incorrect format")
        except Exception as e:
            print(f"Warning during datetime parsing: {e}")

    # Parsing 'score' row to new columns: home_goals, away_goals
    if 'score' in processed_df:
        try:
            processed_df[['home_goals','away_goals']] = processed_df['score'].str.split('–', expand=True).astype('Int64')
            errors_counter = processed_df[['home_goals','away_goals']].isnull().sum().sum()
            if errors_counter > 0:
                print(f"Warning: There's {errors_counter} rows with incorrect format")
        except Exception as e:
            print(f"Warning during score parsing: {e}")
    
    # Creating 'result' column which contains match result (H - home win, A - away win, D - draw)
    if 'home_goals' in processed_df and 'away_goals' in processed_df:
        try:
            conditions = [
                processed_df['home_goals'] > processed_df['away_goals'],
                processed_df['home_goals'] < processed_df['away_goals']
            ]
            choices = ['H', 'A']
            processed_df['result'] = np.select(conditions, choices, default='D')
        except Exception as e:
            print(f"Warning during result calculation: {e}")

    # Drop columns ['date', 'time', 'score']
    columns_to_drop = ['date', 'time', 'score']
    processed_df = processed_df.drop(columns=columns_to_drop, errors='ignore')

    return processed_df