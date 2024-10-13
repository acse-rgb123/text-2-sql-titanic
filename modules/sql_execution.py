import sqlite3
import pandas as pd

def execute_sql_query(db_file, query):
    """Execute SQL query and return result as a DataFrame."""
    conn = sqlite3.connect(db_file)
    try:
        return pd.read_sql_query(query, conn)
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return None
    finally:
        conn.close()
