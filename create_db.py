"""Script para crear la base de datos de SmartSpaces con datos iniciales."""

import sqlite3
import os
from datetime import datetime, timedelta

# Eliminar la base de datos si ya existe (para recrearla limpia)
if os.path.exists("smartspaces.db"):
    os.remove("smartspaces.db")

conn = sqlite3.connect("smartspaces.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# ===========================================================================
# CREAR TABLAS
# ===========================================================================

# Tabla base para todos los espacios (Space y SpaceMeetingRoom)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS spaces (
        space_id     TEXT    PRIMARY KEY,
        space_name   TEXT    NOT NULL,
        capacity     INTEGER NOT NULL,
        space_type   TEXT    NOT NULL,
        space_status TEXT    NOT NULL
    )
""")

# Tabla para los datos extra de SpaceMeetingRoom (herencia → dos tablas relacionadas)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS meeting_rooms (
        space_id          TEXT    PRIMARY KEY,
        room_number       TEXT    NOT NULL,
        floor             INTEGER NOT NULL,
        equipment_list    TEXT    NOT NULL,
        num_power_outlets INTEGER NOT NULL,
        FOREIGN KEY (space_id) REFERENCES spaces(space_id)
    )
""")

# Tabla de usuarios
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id  TEXT PRIMARY KEY,
        name     TEXT    NOT NULL,
        surname1 TEXT    NOT NULL,
        surname2 TEXT    NOT NULL,
        active   INTEGER NOT NULL
    )
""")

# Tabla de reservas
cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id     TEXT PRIMARY KEY,
        space_id       TEXT NOT NULL,
        user_id        TEXT NOT NULL,
        start_time     TEXT NOT NULL,
        end_time       TEXT NOT NULL,
        booking_status TEXT NOT NULL,
        FOREIGN KEY (space_id) REFERENCES spaces(space_id),
        FOREIGN KEY (user_id)  REFERENCES users(user_id)
    )
""")

# ===========================================================================
# INSERTAR ESPACIOS (equivalente a seed_spaces)
# Los Space normales solo van a 'spaces'.
# Los SpaceMeetingRoom van a 'spaces' + 'meeting_rooms'.
# ===========================================================================

# Space("S1", "Conference Room", 5, "Basic")
cursor.execute("INSERT INTO spaces VALUES (?, ?, ?, ?, ?)",
               ("S1", "Conference Room", 5, "Basic", "AVAILABLE"))

# Space("S2", "Open Space", 10, "Basic")
cursor.execute("INSERT INTO spaces VALUES (?, ?, ?, ?, ?)",
               ("S2", "Open Space", 10, "Basic", "AVAILABLE"))

# SpaceMeetingRoom("S3", "Main Meeting Room", 8, "101", 1, ["Projector", "Whiteboard"], 4)
cursor.execute("INSERT INTO spaces VALUES (?, ?, ?, ?, ?)",
               ("S3", "Main Meeting Room", 8, "Meeting room", "AVAILABLE"))
cursor.execute("INSERT INTO meeting_rooms VALUES (?, ?, ?, ?, ?)",
               ("S3", "101", 1, "Projector,Whiteboard", 4))

# SpaceMeetingRoom("S4", "Small Meeting Room", 4, "102", 1, ["TV"], 2)
cursor.execute("INSERT INTO spaces VALUES (?, ?, ?, ?, ?)",
               ("S4", "Small Meeting Room", 4, "Meeting room", "AVAILABLE"))
cursor.execute("INSERT INTO meeting_rooms VALUES (?, ?, ?, ?, ?)",
               ("S4", "102", 1, "TV", 2))

# Space("S5", "Private Office", 2, "Private")
cursor.execute("INSERT INTO spaces VALUES (?, ?, ?, ?, ?)",
               ("S5", "Private Office", 2, "Private", "AVAILABLE"))

# ===========================================================================
# INSERTAR USUARIOS (equivalente a seed_users)
# ===========================================================================

users = [
    ("U1", "Alice",   "Smith",    "Johnson",  1),
    ("U2", "Bob",     "Brown",    "Taylor",   1),
    ("U3", "Charlie", "Wilson",   "Anderson", 1),
    ("U4", "Diana",   "Martinez", "Lopez",    1),
    ("U5", "Eve",     "Davis",    "Clark",    1),
]
cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?)", users)

# ===========================================================================
# INSERTAR RESERVAS (equivalente a seed_bookings)
# Las fechas se guardan como texto ISO 8601.
# ===========================================================================

now = datetime.now()
bookings = [
    ("B1", "S1", "U1",
     (now + timedelta(hours=1)).isoformat(),
     (now + timedelta(hours=2)).isoformat(),
     "ACTIVE"),
    ("B2", "S3", "U2",
     (now + timedelta(days=1)).isoformat(),
     (now + timedelta(days=1, hours=2)).isoformat(),
     "ACTIVE"),
    ("B3", "S2", "U3",
     (now + timedelta(hours=3)).isoformat(),
     (now + timedelta(hours=5)).isoformat(),
     "ACTIVE"),
]
cursor.executemany("INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?)", bookings)

# Actualizar el status de los espacios que quedan reservados
for _, space_id, *_ in bookings:
    cursor.execute(
        "UPDATE spaces SET space_status = 'RESERVED' WHERE space_id = ?",
        (space_id,)
    )

conn.commit()
print("Base de datos creada con datos iniciales.")

# ===========================================================================
# VERIFICACIÓN: mostrar contenido de todas las tablas
# ===========================================================================

print("\n--- Spaces ---")
cursor.execute("SELECT * FROM spaces")
for fila in cursor.fetchall():
    print(f"  {fila[0]} | {fila[1]} | cap:{fila[2]} | tipo:{fila[3]} | estado:{fila[4]}")

print("\n--- Meeting Rooms ---")
cursor.execute("SELECT * FROM meeting_rooms")
for fila in cursor.fetchall():
    print(f"  {fila[0]} | sala:{fila[1]} | planta:{fila[2]} | equipamiento:{fila[3]} | enchufes:{fila[4]}")

print("\n--- Users ---")
cursor.execute("SELECT * FROM users")
for fila in cursor.fetchall():
    activo = "activo" if fila[4] else "inactivo"
    print(f"  {fila[0]} | {fila[1]} {fila[2]} {fila[3]} | {activo}")

print("\n--- Bookings ---")
cursor.execute("SELECT * FROM bookings")
for fila in cursor.fetchall():
    print(f"  {fila[0]} | espacio:{fila[1]} | usuario:{fila[2]} | {fila[3][:16]} → {fila[4][11:16]} | {fila[5]}")

conn.close()
print("\nBase de datos guardada en smartspaces.db")