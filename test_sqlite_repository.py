"""test_sqlite_repository.py

Prueba del repositorio SQLite de espacios adaptado al proyecto SmartSpaces real.
Ejecutar desde la raíz del proyecto: python test_sqlite_repository.py
"""

from domain.space import Space
from domain.space_meetingroom import SpaceMeetingRoom
from infrastructure.space_sqlite_repository import SpaceSQLiteRepository
from infrastructure.exceptions import (
    SpaceAlreadyExistsException,
    SpaceNotFoundError,
)

repo = SpaceSQLiteRepository("smartspaces.db")

# --- Prueba 1: Obtener espacio existente (Space básico) ---
print("--- Prueba 1: Obtener espacio existente ---")
try:
    espacio = repo.get("S1")
    print(f"✓ {espacio.space_id} - {espacio.space_name} - Cap: {espacio.capacity} - Estado: {espacio.space_status}")
except SpaceNotFoundError as e:
    print(f"✗ {e}")

# --- Prueba 2: Obtener SpaceMeetingRoom existente ---
print("\n--- Prueba 2: Obtener SpaceMeetingRoom existente ---")
try:
    sala = repo.get("S3")
    tipo = "SpaceMeetingRoom" if isinstance(sala, SpaceMeetingRoom) else "Space"
    print(f"✓ {sala.space_id} - {sala.space_name} [{tipo}]")
    if isinstance(sala, SpaceMeetingRoom):
        print(f"   Sala: {sala.room_number}, Planta: {sala.floor}, Equipamiento: {sala.equipment_list}")
except SpaceNotFoundError as e:
    print(f"✗ {e}")

# --- Prueba 3: Espacio inexistente ---
print("\n--- Prueba 3: Espacio no encontrado ---")
try:
    repo.get("INEXISTENTE")
except SpaceNotFoundError as e:
    print(f"✓ Error esperado: {e}")

# --- Prueba 4: Guardar Space nuevo ---
print("\n--- Prueba 4: Guardar Space nuevo ---")
try:
    nuevo = Space("TEST01", "Espacio Prueba", 6)
    repo.save(nuevo)
    print("✓ Space TEST01 guardado correctamente")
except SpaceAlreadyExistsException as e:
    print(f"✗ {e}")

# --- Prueba 5: Guardar SpaceMeetingRoom nuevo ---
print("\n--- Prueba 5: Guardar SpaceMeetingRoom nuevo ---")
try:
    nueva_sala = SpaceMeetingRoom("TEST02", "Sala Prueba", 10, "201", 2, ["Projector", "TV"], 6)
    repo.save(nueva_sala)
    print("✓ SpaceMeetingRoom TEST02 guardada correctamente")
except SpaceAlreadyExistsException as e:
    print(f"✗ {e}")

# --- Prueba 6: Intentar guardar duplicado ---
print("\n--- Prueba 6: Duplicado ---")
try:
    duplicado = Space("S1", "Duplicado", 5)
    repo.save(duplicado)
except SpaceAlreadyExistsException as e:
    print(f"✓ Error esperado: {e}")

# --- Prueba 7: Listar todos los espacios ---
print("\n--- Prueba 7: Listar todos los espacios ---")
espacios = repo.list()
for esp in espacios:
    tipo = "SpaceMeetingRoom" if isinstance(esp, SpaceMeetingRoom) else "Space"
    print(f"  {esp.space_id}: {esp.space_name} (Cap: {esp.capacity}) [{tipo}]")

# --- Prueba 8: Actualizar Space ---
print("\n--- Prueba 8: Actualizar Space ---")
actualizado = repo.get("TEST01")
actualizado.space_name = "Espacio Prueba Actualizado"
actualizado.capacity = 8
repo.update(actualizado)
recuperado = repo.get("TEST01")
print(f"✓ Actualizado: {recuperado.space_name}, Cap: {recuperado.capacity}")

# --- Prueba 9: Eliminar espacios de prueba ---
print("\n--- Prueba 9: Eliminar espacios de prueba ---")
repo.delete("TEST01")
repo.delete("TEST02")
try:
    repo.get("TEST01")
except SpaceNotFoundError as e:
    print(f"✓ Eliminado correctamente: {e}")

print("\n✓ Todas las pruebas completadas")