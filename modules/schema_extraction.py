import sqlite3

def extract_schema_from_db(db_file):
    """Extract schema metadata from the SQLite database."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema[table_name] = {col[1]: col[2] for col in columns}
    
    conn.close()
    return schema
