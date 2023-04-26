import sqlite3

conn = sqlite3.connect("blurring.db")

columns = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "status VARCHAR NOT NULL",
    "result TEXT",
    "nb_of_completed_process INTEGER NOT NULL",
    "nb_of_total_process INTEGER NOT NULL",
    "error_message TEXT",
    "created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP",
    "updated_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP",
]
create_table_cmd = f"CREATE TABLE blurring_run ({','.join(columns)})"
conn.execute(create_table_cmd)
