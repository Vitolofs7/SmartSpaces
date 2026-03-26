import sqlite3

conn = sqlite3.connect("smartspaces.db")
try:
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO spaces VALUES ('S1', 'Duplicated Space', 5, 'Basic', 'AVAILABLE')"
        )
except sqlite3.IntegrityError as e:
    print(f"IntegrityError: {e}")
finally:
    conn.close()

conn = sqlite3.connect("smartspaces.db")
try:
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO spaces VALUES (?, ?, ?, ?, ?)",
            ("T1", None, 5, "Basic", "AVAILABLE"),
        )
except sqlite3.IntegrityError as e:
    print(f"Integrit Error por None: {e}")
finally:
    conn.close()

conn = sqlite3.connect("smartspaces.db")
try:
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas")   ## tabla inexistente
except sqlite3.OperationalError as e:
    print(f"OperationalError: {e}")
finally:
    conn.close()