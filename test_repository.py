from domain.space import Space
from domain.space_meetingroom import SpaceMeetingRoom
from infrastructure.repository_sqlite import RepositorioSpacesSQLite
from infrastructure.errors import SpaceAlreadyExistsError, SpaceNotFoundError, PersistenceError

repo = RepositorioSpacesSQLite("smartspaces.db")

# --- Test guardar y obtener ---
space = Space("T2", "Test Room", 4, "Basic")
try:
    repo.save(space)
    print("Space T2 saved successfully.")
except SpaceAlreadyExistsError as e:
    print(f"Already exists: {e}")
except PersistenceError as e:
    print(f"Persistence error: {e}")

space_loaded = repo.give("T2")
print(f"Loaded: {space_loaded.space_id} - {space_loaded.space_name} - status:{space_loaded.space_status}")

# --- Test actualizar ---
space_loaded.capacity = 10
repo.update(space_loaded)
space_updated = repo.give("T2")
print(f"Updated capacity: {space_updated.capacity}")  # debe ser 10

# --- Test listar ---
all_spaces = repo.list()
print(f"Total spaces: {len(all_spaces)}")

# --- Test eliminar ---
repo.delete("T2")
try:
    repo.give("T2")
except SpaceNotFoundError as e:
    print(f"Expected error after delete: {e}")