import duckdb
import pandas as pd
from pathlib import Path

CSV_FILE = Path("data") / "people.csv"

def load_data():
    con = duckdb.connect()
    try:
        return con.execute(
            """
            SELECT first_name,last_name,gender,dob,title
            FROM read_csv_auto(?)
            LIMIT 5
            """,
            [str(CSV_FILE)]
        ).df()
    finally:
        con.close()


def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"{CSV_FILE} not found")

    df = load_data()
    
    if df.empty:
        print("No data found in CSV")
        return
    
    print("*" * 50)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()