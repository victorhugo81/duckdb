# DuckDB CSV Reader Example

This project is a simple Python script that demonstrates how to use **DuckDB** to read data directly from a CSV file and load it into a **Pandas DataFrame** for easy inspection.

The script reads a CSV file containing people data, selects specific columns, limits the result to a few rows, and prints the output to the console.

---

## Project Structure

```
.
├── data/
│   └── people.csv
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

* **data/people.csv** – Input CSV file containing people data
* **main.py** – Python script that loads and queries the CSV using DuckDB
* **README.md** – Project documentation

---

## Requirements

* Python **3.13+**
* [uv](https://docs.astral.sh/uv/) (install on macOS with `brew install uv`)

Dependencies (`duckdb`, `pandas`) are declared in `pyproject.toml` and pinned in `uv.lock`. Install them into a project virtual environment (`.venv/`) with:

```bash
uv sync
```

> **Troubleshooting:** If you see `ModuleNotFoundError: No module named 'duckdb'`, you ran the script with your system Python instead of the project environment. Run `uv sync`, then use `uv run python main.py` (or activate the environment first with `source .venv/bin/activate` and then run `python3 main.py`).

---

## CSV File Requirements

The `people.csv` file must exist in the `data/` directory and include at least the following columns:

* `first_name`
* `last_name`
* `gender`
* `dob`
* `title`

Example:

```csv
first_name,last_name,gender,dob,title
John,Doe,M,1985-01-15,Engineer
Jane,Smith,F,1990-06-20,Manager
```

---

## ▶How to Run

From the project root directory, run:

```bash
uv run python main.py                    # preview 5 rows, then run every query
uv run python main.py top_titles         # run one (or several) queries by name
uv run python main.py --list             # list available queries
```

Available queries: `gender_counts`, `top_titles`, `oldest_people`, `born_by_decade`, `email_domains`, `average_age_by_gender`. To add your own, add an entry to the `QUERIES` dict in `main.py` and select `FROM people`.

---

## What the Script Does

1. Verifies that `data/people.csv` exists
2. Uses DuckDB’s `read_csv_auto()` to query the CSV directly (no database setup required)
3. Selects specific columns
4. Limits the result to **5 rows**
5. Converts the result into a Pandas DataFrame
6. Prints the output in a clean, tabular format

---

## Example Output

```
**************************************************
first_name last_name gender        dob       title
John       Doe       M      1985-01-15  Engineer
Jane       Smith     F      1990-06-20   Manager
```

---

## Why DuckDB?

* No server or setup required
* Fast analytical queries on CSV files
* SQL-based querying
* Seamless integration with Pandas

---

## Notes

* DuckDB creates an in-memory database by default
* The database connection is safely closed after each query
* This script is ideal for quick data exploration and prototyping

---

## License

This project is provided for educational and internal use. Add a license if you plan to distribute it publicly.

