import pandas as pd
from src.infrastructure.database import read_from_db, save_to_db
from src.processing.cleaner.data_cleaning import inspect_table_data, clean_raw_data

def main():
    db = read_from_db("SELECT * FROM raw_historical_schedules")
    # inspect_table_data("raw_historical_schedules")
    processed_db = clean_raw_data(db)
    print("\n" + "="*40)
    print("KOLUMNY W PRZETWORZONYM DATAFRAME:")
    print("="*40)
    print(processed_db.columns.tolist())
    
    print("\n" + "="*40)
    print("PIERWSZE 3 WIERSZE PO CZYSZCZENIU:")
    print("="*40)
    print(processed_db.head(3))

    processed_table="processed_historical_schedules"
    save_to_db(processed_db, processed_table)

if __name__ == "__main__":
    main()