"""Query data/people.csv with DuckDB.

Usage:
    uv run python main.py            # preview rows, then run every query
    uv run python main.py <name>     # run one or more queries by name, e.g. `gender_counts`
    uv run python main.py --list     # list available queries
"""

import sys
from pathlib import Path

import duckdb

CSV_FILE = Path("data") / "people.csv"

# Each query reads from the `people` view created in run_queries().
QUERIES = {
    "gender_counts": """
        SELECT gender, COUNT(*) AS people
        FROM people
        GROUP BY gender
        ORDER BY people DESC
    """,
    "top_titles": """
        SELECT title, COUNT(*) AS people
        FROM people
        GROUP BY title
        ORDER BY people DESC, title
        LIMIT 10
    """,
    "oldest_people": """
        SELECT first_name, last_name, dob,
               date_diff('year', dob, current_date) AS age
        FROM people
        ORDER BY dob
        LIMIT 5
    """,
    "born_by_decade": """
        SELECT (year(dob) // 10) * 10 AS decade, COUNT(*) AS people
        FROM people
        GROUP BY decade
        ORDER BY decade
    """,
    "email_domains": """
        SELECT split_part(email, '@', 2) AS domain, COUNT(*) AS people
        FROM people
        GROUP BY domain
        ORDER BY people DESC
    """,
    "average_age_by_gender": """
        SELECT gender,
               ROUND(AVG(date_diff('year', dob, current_date)), 1) AS avg_age,
               MIN(dob) AS earliest_dob,
               MAX(dob) AS latest_dob
        FROM people
        GROUP BY gender
        ORDER BY gender
    """,
}


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


def run_queries(names):
    con = duckdb.connect()
    try:
        con.execute(
            f"CREATE VIEW people AS SELECT * FROM read_csv_auto('{CSV_FILE.as_posix()}')"
        )
        for name in names:
            df = con.execute(QUERIES[name]).df()
            print(f"\n=== {name} ===")
            print(df.to_string(index=False))
    finally:
        con.close()


def main():
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"{CSV_FILE} not found")

    args = sys.argv[1:]
    if args == ["--list"]:
        print("\n".join(QUERIES))
        return

    unknown = [a for a in args if a not in QUERIES]
    if unknown:
        sys.exit(f"Unknown query: {', '.join(unknown)}. Available: {', '.join(QUERIES)}")

    if args:
        run_queries(args)
        return

    df = load_data()

    if df.empty:
        print("No data found in CSV")
        return

    print("*" * 50)
    print(df.to_string(index=False))

    run_queries(list(QUERIES))


if __name__ == "__main__":
    main()
