# SmartSpaces - Database Design Document

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Principios de Diseño](#principios-de-diseño)
3. [Esquema de Base de Datos](#esquema-de-base-de-datos)
4. [Entidades y Relaciones](#entidades-y-relaciones)
5. [Índices y Optimizaciones](#índices-y-optimizaciones)
6. [Estrategia de Persistencia](#estrategia-de-persistencia)
7. [Consultas Principales](#consultas-principales)
8. [Consideraciones de Integridad](#consideraciones-de-integridad)
9. [Migraciones y Versionado](#migraciones-y-versionado)

---

## 🎯 Visión General

SmartSpaces utiliza **SQLite 3** como motor de persistencia. La base de datos está diseñada siguiendo una **arquitectura limpia de capas**, donde:

- **Dominio**: Contiene la lógica de negocio y las validaciones
- **Infraestructura**: Mapea objetos de dominio a tablas SQLite
- **Presentación**: Captura excepciones de dominio, no de BD

### Características Principales

- ✅ **Relaciones entre entidades** mediante claves foráneas
- ✅ **Herencia Mapeada a Tabla Separada** (Space → SpaceMeetingRoom)
- ✅ **Integridad Referencial** con `PRAGMA foreign_keys = ON`
- ✅ **Excepciones de Dominio** transformadas desde errores SQLite
- ✅ **Timestamps ISO 8601** para formato universal de fechas
- ✅ **Sin dependencias externas** (SQLite incluido en Python stdlib)

---

## 🏗️ Principios de Diseño

### 1. Mapeo ORM Manual

SmartSpaces **no usa ORM frameworks** (como SQLAlchemy). El mapeo es **manual y explícito**:

```
Dominio (Python)          ↔  Base de Datos (SQLite)
─────────────────────────────────────────────────
Space object              ↔  spaces (table)
SpaceMeetingRoom object   ↔  spaces + meeting_rooms (herencia)
Booking object            ↔  bookings (table)
User object               ↔  users (table)
```

**Ventaja**: Control total sobre transformaciones y excepciones.

### 2. Herencia: Single Table + Specialized Table

La clase `SpaceMeetingRoom` hereda de `Space`:

```python
class Space: ...
class SpaceMeetingRoom(Space): ...
```

**Mapeo en BD**:
- `spaces`: Tabla base con campos comunes (space_id, space_name, capacity, space_type, space_status)
- `meeting_rooms`: Tabla especializada con FOREIGN KEY a spaces.space_id

**Ventaja**: Flexibilidad. Un Space puede existir sin datos de MeetingRoom, pero MeetingRoom siempre requiere Space.

### 3. Timestamps ISO 8601

Las fechas se almacenan como **strings ISO 8601** en la columna `TEXT`:

```python
from datetime import datetime

# Guardar en BD
start_time_str = start_time.isoformat()  # "2025-04-22T14:30:00.123456"

# Recuperar de BD
start_time = datetime.fromisoformat(start_time_str)
```

**Ventaja**: Universal, portable, legible en cualquier sistema.

### 4. Enums Almacenados como Strings

Estados y tipos se almacenan como valores string constantes:

```sql
-- space_status: "AVAILABLE", "RESERVED", "MAINTENANCE"
-- booking_status: "ACTIVE", "CANCELLED", "FINISHED"
```

**Ventaja**: Legibilidad directa en SQL. Fácil de auditar y debuggear.

### 5. IDs Autogenerados Inteligentes

Los repositorios asignan IDs automáticamente si `None`:

```python
# Space regular: S1, S2, S3, ...
# SpaceMeetingRoom: SM1, SM2, SM3, ...
# User: U1, U2, U3, ...
# Booking: B1, B2, B3, ...
```

**Ventaja**: IDs con significado semántico. Fácil identificar tipo desde ID.

---

## 📊 Esquema de Base de Datos

### Diagrama Entidad-Relación

```
┌─────────────────────────────────────────────────────────────┐
│                    SPACES                                   │
├──────────────────────────────────────────────────────────────┤
│ PK │ space_id      TEXT                                      │
│    │ space_name    TEXT NOT NULL                             │
│    │ capacity      INTEGER NOT NULL (> 0)                    │
│    │ space_type    TEXT NOT NULL                             │
│    │ space_status  TEXT NOT NULL (AVAILABLE|RESERVED|...)    │
└──────────────────────────────────────────────────────────────┘
              │
              │ FK space_id (1:1)
              │
              ↓
┌──────────────────────────────────────────────────────────────┐
│              MEETING_ROOMS (Herencia)                        │
├──────────────────────────────────────────────────────────────┤
│ PK │ space_id            TEXT (FK → spaces)                  │
│    │ room_number         TEXT NOT NULL                       │
│    │ floor               INTEGER NOT NULL                    │
│    │ equipment_list      TEXT (comma-separated)              │
│    │ num_power_outlets   INTEGER NOT NULL (≥ 0)             │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    USERS                                     │
├──────────────────────────────────────────────────────────────┤
│ PK │ user_id    TEXT                                         │
│    │ name       TEXT NOT NULL                                │
│    │ surname1   TEXT NOT NULL                                │
│    │ surname2   TEXT NOT NULL                                │
│    │ active     INTEGER NOT NULL (0|1, default=1)           │
└──────────────────────────────────────────────────────────────┘
              │
              │ FK user_id (1:N)
              │
              ↓
┌──────────────────────────────────────────────────────────────┐
│                    BOOKINGS                                  │
├──────────────────────────────────────────────────────────────┤
│ PK │ booking_id       TEXT                                   │
│    │ space_id         TEXT NOT NULL (FK → spaces)            │
│    │ user_id          TEXT NOT NULL (FK → users)             │
│    │ start_time       TEXT NOT NULL (ISO 8601)               │
│    │ end_time         TEXT NOT NULL (ISO 8601)               │
│    │ booking_status   TEXT NOT NULL (ACTIVE|CANCELLED|...)   │
└──────────────────────────────────────────────────────────────┘
              ↑
         FK space_id
              │
         (1:N relationship)
```

---

## 🔗 Entidades y Relaciones

### 1. Tabla `spaces`

**Propósito**: Almacenar todos los espacios (genéricos y especializados).

| Columna | Tipo | Restricciones | Dominio | Notas |
|---------|------|---------------|---------|-------|
| `space_id` | TEXT | PRIMARY KEY | S1, S2, S3... | Alfanumérico, inmutable |
| `space_name` | TEXT | NOT NULL | Max 255 | Nombre del espacio |
| `capacity` | INTEGER | NOT NULL, > 0 | 1-1000 | Capacidad máxima |
| `space_type` | TEXT | NOT NULL | "Basic Space", "Meeting room", "Private" | Clasificación |
| `space_status` | TEXT | NOT NULL | "AVAILABLE", "RESERVED", "MAINTENANCE" | Estado actual |

**Claves Foráneas**: Ninguna (tabla raíz)

**Índices Recomendados**:
```sql
CREATE INDEX idx_spaces_status ON spaces(space_status);
CREATE INDEX idx_spaces_type ON spaces(space_type);
```

**Cardinalidad Esperada**: 5-50 registros

---

### 2. Tabla `meeting_rooms` (Herencia)

**Propósito**: Datos especializados para espacios tipo "Sala de Reuniones".

| Columna | Tipo | Restricciones | Dominio | Notas |
|---------|------|---------------|---------|-------|
| `space_id` | TEXT | PRIMARY KEY, FK | SM1, SM2... | Referencia a spaces |
| `room_number` | TEXT | NOT NULL | "101", "201"... | Ubicación física |
| `floor` | INTEGER | NOT NULL, ≥ 0 | 1-10 | Planta del edificio |
| `equipment_list` | TEXT | NOT NULL | "Projector,Whiteboard,TV" | Equipamiento (CSV) |
| `num_power_outlets` | INTEGER | NOT NULL, ≥ 0 | 0-20 | Enchufes disponibles |

**Claves Foráneas**:
```sql
FOREIGN KEY (space_id) REFERENCES spaces(space_id)
```

**Cardinalidad Esperada**: 0-10 registros (subconjunto de spaces)

**Notas sobre Herencia**:
- Un registro en `meeting_rooms` implica que existe en `spaces`
- Un Space puede no tener registro en `meeting_rooms` (es genérico)
- El repositorio reconstruye automáticamente el tipo correcto al recuperar

---

### 3. Tabla `users`

**Propósito**: Almacenar información de usuarios que pueden hacer reservas.

| Columna | Tipo | Restricciones | Dominio | Notas |
|---------|------|---------------|---------|-------|
| `user_id` | TEXT | PRIMARY KEY | U1, U2, U3... | Alfanumérico, inmutable |
| `name` | TEXT | NOT NULL | Max 100 | Nombre de pila |
| `surname1` | TEXT | NOT NULL | Max 100 | Primer apellido |
| `surname2` | TEXT | NOT NULL | Max 100 | Segundo apellido |
| `active` | INTEGER | NOT NULL | 0 (inactivo) ó 1 (activo) | Estado de cuenta |

**Claves Foráneas**: Ninguna (tabla raíz)

**Índices Recomendados**:
```sql
CREATE INDEX idx_users_active ON users(active);
CREATE INDEX idx_users_name ON users(name, surname1, surname2);
```

**Cardinalidad Esperada**: 10-1000 registros

**Restricciones de Negocio**:
- Un usuario inactivo (`active = 0`) no puede crear nuevas reservas
- Puede tener múltiples reservas activas (limitadas por max_active_bookings)
- Máximo duración de reserva: 2 horas

---

### 4. Tabla `bookings`

**Propósito**: Gestionar reservas de espacios por usuarios.

| Columna | Tipo | Restricciones | Dominio | Notas |
|---------|------|---------------|---------|-------|
| `booking_id` | TEXT | PRIMARY KEY | B1, B2, B3... | Alfanumérico |
| `space_id` | TEXT | NOT NULL, FK | S1, SM1... | Referencia a spaces |
| `user_id` | TEXT | NOT NULL, FK | U1, U2... | Referencia a users |
| `start_time` | TEXT | NOT NULL | ISO 8601 | "2025-04-22T14:30:00" |
| `end_time` | TEXT | NOT NULL | ISO 8601 | "2025-04-22T16:30:00" |
| `booking_status` | TEXT | NOT NULL | "ACTIVE", "CANCELLED", "FINISHED" | Estado de la reserva |

**Claves Foráneas**:
```sql
FOREIGN KEY (space_id) REFERENCES spaces(space_id) ON DELETE RESTRICT,
FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
```

**Índices Recomendados**:
```sql
CREATE INDEX idx_bookings_space ON bookings(space_id);
CREATE INDEX idx_bookings_user ON bookings(user_id);
CREATE INDEX idx_bookings_status ON bookings(booking_status);
CREATE INDEX idx_bookings_time ON bookings(start_time, end_time);
```

**Cardinalidad Esperada**: 50-10000 registros

**Restricciones de Negocio**:
- `start_time < end_time` (validado en dominio)
- No se permiten solapamientos entre reservas ACTIVAS del mismo espacio
- Un usuario INACTIVO no puede crear reservas
- Un espacio en MAINTENANCE no puede ser reservado
- Un espacio RESERVED puede tener múltiples reservas si no solapan en tiempo

---

## 🔐 Índices y Optimizaciones

### Índices Críticos

```sql
-- Búsquedas por estado (queries frecuentes)
CREATE INDEX idx_spaces_status ON spaces(space_status);
CREATE INDEX idx_bookings_status ON bookings(booking_status);
CREATE INDEX idx_users_active ON users(active);

-- Búsquedas por foreign key (joins)
CREATE INDEX idx_bookings_space ON bookings(space_id);
CREATE INDEX idx_bookings_user ON bookings(user_id);

-- Búsquedas por tiempo (para detectar solapamientos)
CREATE INDEX idx_bookings_time ON bookings(start_time, end_time);

-- Búsquedas por nombre (reportes)
CREATE INDEX idx_users_name ON users(name, surname1, surname2);
```

### Estrategia de Búsqueda de Solapamientos

Para detectar si una nueva reserva B1 [start1, end1] solaparía con existentes:

```sql
SELECT * FROM bookings
WHERE space_id = ?
  AND booking_status = 'ACTIVE'
  AND start_time < ?   -- end1
  AND end_time > ?     -- start1
```

**Sin solapamiento si**: `start1 >= end_existing` O `end1 <= start_existing`

**Con solapamiento si**: `start1 < end_existing` AND `end1 > start_existing`

---

## 💾 Estrategia de Persistencia

### Ciclo de Vida del Repositorio

```python
class SpaceSQLiteRepository:
    def __init__(self, db_path: str = "smartspaces.db"):
        self._db_path = db_path
    
    def _connect(self):
        """Crea conexión con PRAGMA foreign_keys = ON"""
        conn = sqlite3.connect(self._db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
```

### Operaciones CRUD

#### 1. CREATE (save)

```python
def save(self, space: Space) -> None:
    conn = self._connect()
    try:
        with conn:  # Auto-commit si OK, rollback si error
            cursor = conn.cursor()
            
            # Auto-generar ID si es None
            if space.space_id is None:
                max_id = cursor.execute(
                    "SELECT MAX(CAST(SUBSTR(space_id, 2) AS INTEGER)) FROM spaces"
                ).fetchone()[0] or 0
                space.space_id = f"S{max_id + 1}"
            
            # INSERT en spaces
            cursor.execute(
                "INSERT INTO spaces VALUES (?, ?, ?, ?, ?)",
                (space.space_id, space.space_name, space.capacity, space.space_type, space.space_status)
            )
            
            # Si es MeetingRoom, INSERT en meeting_rooms también
            if isinstance(space, SpaceMeetingRoom):
                equipment_str = ",".join(space.equipment_list)
                cursor.execute(
                    "INSERT INTO meeting_rooms VALUES (?, ?, ?, ?, ?)",
                    (space.space_id, space.room_number, space.floor, equipment_str, space.num_power_outlets)
                )
    except sqlite3.IntegrityError:
        raise SpaceAlreadyExistsException(f"Space {space.space_id} already exists")
    except sqlite3.OperationalError as e:
        raise PersistenceException(f"Database error: {e}")
    finally:
        conn.close()
```

**Excepciones Transformadas**:
- `IntegrityError` (PRIMARY KEY duplicada) → `SpaceAlreadyExistsException`
- `OperationalError` (tabla inexistente, permisos) → `PersistenceException`

#### 2. READ (get)

```python
def get(self, space_id: str) -> Space:
    conn = self._connect()
    try:
        cursor = conn.cursor()
        
        # SELECT de spaces
        cursor.execute(
            "SELECT space_id, space_name, capacity, space_type, space_status FROM spaces WHERE space_id = ?",
            (space_id,)
        )
        row = cursor.fetchone()
        
        if row is None:
            raise SpaceNotFoundError(f"Space {space_id} not found")
        
        sid, name, capacity, space_type, status = row
        
        # LEFT JOIN con meeting_rooms
        cursor.execute(
            "SELECT room_number, floor, equipment_list, num_power_outlets FROM meeting_rooms WHERE space_id = ?",
            (sid,)
        )
        mr_row = cursor.fetchone()
        
        # Reconstruir objeto especializado
        if mr_row:
            room_number, floor, equipment_str, num_outlets = mr_row
            equipment_list = equipment_str.split(",") if equipment_str else []
            obj = SpaceMeetingRoom(
                space_id=sid, space_name=name, capacity=capacity,
                room_number=room_number, floor=floor,
                equipment_list=equipment_list, num_power_outlets=num_outlets
            )
        else:
            obj = Space(space_id=sid, space_name=name, capacity=capacity, space_type=space_type)
        
        obj._space_status = status
        return obj
    
    except sqlite3.OperationalError as e:
        raise PersistenceException(f"Database error: {e}")
    finally:
        conn.close()
```

**Características**:
- ✅ Lanza excepción si no encuentra (nunca devuelve None)
- ✅ Reconstruye automáticamente tipo correcto (Space vs SpaceMeetingRoom)
- ✅ Respeta propiedades privadas (`_space_status`)

#### 3. UPDATE (update)

```python
def update(self, space: Space) -> None:
    conn = self._connect()
    try:
        with conn:
            cursor = conn.cursor()
            
            # Validar que existe
            cursor.execute("SELECT space_id FROM spaces WHERE space_id = ?", (space.space_id,))
            if not cursor.fetchone():
                raise SpaceNotFoundError(f"Space {space.space_id} not found")
            
            # UPDATE spaces
            cursor.execute(
                "UPDATE spaces SET space_name = ?, capacity = ?, space_type = ?, space_status = ? WHERE space_id = ?",
                (space.space_name, space.capacity, space.space_type, space.space_status, space.space_id)
            )
            
            # Si es MeetingRoom, UPDATE meeting_rooms
            if isinstance(space, SpaceMeetingRoom):
                equipment_str = ",".join(space.equipment_list)
                cursor.execute(
                    "UPDATE meeting_rooms SET room_number = ?, floor = ?, equipment_list = ?, num_power_outlets = ? WHERE space_id = ?",
                    (space.room_number, space.floor, equipment_str, space.num_power_outlets, space.space_id)
                )
    
    except sqlite3.OperationalError as e:
        raise PersistenceException(f"Database error: {e}")
    finally:
        conn.close()
```

#### 4. DELETE (delete)

```python
def delete(self, space_id: str) -> None:
    conn = self._connect()
    try:
        with conn:
            cursor = conn.cursor()
            
            # Las claves foráneas con ON DELETE CASCADE eliminarían meeting_rooms automáticamente
            # Pero aquí las borramos explícitamente para control
            cursor.execute("DELETE FROM meeting_rooms WHERE space_id = ?", (space_id,))
            cursor.execute("DELETE FROM spaces WHERE space_id = ?", (space_id,))
    
    except sqlite3.OperationalError as e:
        raise PersistenceException(f"Database error: {e}")
    finally:
        conn.close()
```

#### 5. LIST (list)

```python
def list(self) -> list:
    conn = self._connect()
    espacios = []
    try:
        cursor = conn.cursor()
        
        # LEFT JOIN spaces + meeting_rooms
        cursor.execute("""
            SELECT 
                s.space_id, s.space_name, s.capacity, s.space_type, s.space_status,
                mr.room_number, mr.floor, mr.equipment_list, mr.num_power_outlets
            FROM spaces s
            LEFT JOIN meeting_rooms mr ON s.space_id = mr.space_id
        """)
        
        for row in cursor.fetchall():
            sid, name, capacity, space_type, status = row[:5]
            room_number, floor, equipment_str, num_outlets = row[5:]
            
            if room_number is not None:
                equipment_list = equipment_str.split(",") if equipment_str else []
                obj = SpaceMeetingRoom(
                    space_id=sid, space_name=name, capacity=capacity,
                    room_number=room_number, floor=floor,
                    equipment_list=equipment_list, num_power_outlets=num_outlets
                )
            else:
                obj = Space(space_id=sid, space_name=name, capacity=capacity, space_type=space_type)
            
            obj._space_status = status
            espacios.append(obj)
        
        return espacios
    
    except sqlite3.OperationalError as e:
        raise PersistenceException(f"Database error: {e}")
    finally:
        conn.close()
```

---

## 🔍 Consultas Principales

### Consultas Frecuentes

#### 1. Encontrar espacios disponibles en una fecha/hora

```sql
-- Espacios que NO tienen reservas ACTIVAS que solapen
SELECT DISTINCT s.* 
FROM spaces s
LEFT JOIN bookings b ON s.space_id = b.space_id 
    AND b.booking_status = 'ACTIVE'
    AND b.start_time < ?     -- end_time de búsqueda
    AND b.end_time > ?       -- start_time de búsqueda
WHERE s.space_status != 'MAINTENANCE'
  AND b.booking_id IS NULL;
```

#### 2. Listar reservas activas de un usuario

```sql
SELECT b.*, s.space_name, u.name
FROM bookings b
JOIN spaces s ON b.space_id = s.space_id
JOIN users u ON b.user_id = u.user_id
WHERE u.user_id = ?
  AND b.booking_status = 'ACTIVE'
ORDER BY b.start_time;
```

#### 3. Detectar solapamientos para un espacio

```sql
SELECT COUNT(*) as overlaps
FROM bookings
WHERE space_id = ?
  AND booking_status = 'ACTIVE'
  AND start_time < ?      -- end_time de nueva reserva
  AND end_time > ?        -- start_time de nueva reserva
```

#### 4. Historial de reservas de un espacio

```sql
SELECT b.*, u.name, u.surname1, u.surname2
FROM bookings b
JOIN users u ON b.user_id = u.user_id
WHERE b.space_id = ?
ORDER BY b.start_time DESC;
```

#### 5. Espacios con mayor demanda

```sql
SELECT s.space_id, s.space_name, COUNT(b.booking_id) as total_bookings
FROM spaces s
LEFT JOIN bookings b ON s.space_id = b.space_id
GROUP BY s.space_id
ORDER BY total_bookings DESC;
```

---

## ✅ Consideraciones de Integridad

### Integridad Referencial

**PRAGMA foreign_keys = ON** se activa en cada conexión:

```python
conn = sqlite3.connect("smartspaces.db")
conn.execute("PRAGMA foreign_keys = ON")
```

**Restricciones Activas**:

| Restricción | Acción | Efecto |
|-------------|--------|--------|
| `bookings.space_id → spaces.space_id` | ON DELETE RESTRICT | No se puede eliminar un espacio con reservas |
| `bookings.user_id → users.user_id` | ON DELETE RESTRICT | No se puede eliminar un usuario con reservas |
| `meeting_rooms.space_id → spaces.space_id` | ON DELETE CASCADE | Si se elimina un Space, se elimina su MeetingRoom |

### Restricciones de Negocio

#### En el Dominio (Python)

```python
# Space
- capacity > 0
- space_status in ["AVAILABLE", "RESERVED", "MAINTENANCE"]
- Un Space no puede cambiar de ID

# Booking
- start_time < end_time
- No solapamientos con ACTIVE bookings para el mismo espacio
- Usuario debe estar ACTIVO para crear reserva
- Espacio no debe estar en MAINTENANCE

# User
- Todos los campos no vacíos
- max_active_bookings = 1 (límite por usuario)
- max_booking_duration = 2 horas
- Usuario inactivo no puede crear reservas
```

#### En la Base de Datos (SQL)

```sql
-- Capacidad positiva (no enforced en SQLite, pero en dominio)
-- CHECK (capacity > 0) -- SQLite 3.8.2+

-- Estados válidos (no enforced en SQLite, pero en dominio)
-- CHECK (space_status IN ('AVAILABLE', 'RESERVED', 'MAINTENANCE'))

-- Claves foráneas (enforced con PRAGMA foreign_keys = ON)
FOREIGN KEY (space_id) REFERENCES spaces(space_id)
FOREIGN KEY (user_id) REFERENCES users(user_id)
```

### Consistencia Transaccional

El patrón `with conn:` garantiza:

```python
with conn:
    # Todas las operaciones en el bloque son transacionales
    cursor.execute(INSERT_STATEMENT_1)
    cursor.execute(INSERT_STATEMENT_2)
    # Si OK → COMMIT automático
    # Si error → ROLLBACK automático
```

**Ejemplo**: Al crear una `SpaceMeetingRoom`:
1. INSERT en `spaces`
2. INSERT en `meeting_rooms` (con FK a spaces.space_id)
3. Si el INSERT #2 falla, ambos se revierten

---

## 🔄 Migraciones y Versionado

### Versionado de Esquema

El archivo `create_db.py` es la "versión 1.0" del esquema:

```python
# create_db.py versión 1.0
# - spaces: PK space_id
# - meeting_rooms: FK a spaces
# - users: PK user_id
# - bookings: FK a spaces y users
```

### Estrategia de Evolución

Para cambios futuros:

```python
# Versión 2.0: Agregar timestamps de auditoría
# ALTER TABLE spaces ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP;
# ALTER TABLE bookings ADD COLUMN updated_at TEXT;

# Versión 2.1: Agregar índices de optimización
# CREATE INDEX idx_bookings_user_status ON bookings(user_id, booking_status);
```

### Recreación de BD en Desarrollo

```bash
# Elimina y recrea limpia
python create_db.py

# Populate con datos iniciales
python -c "from infrastructure.seed_data import seed_all; seed_all()"
```

---

## 🛡️ Manejo de Excepciones en Capa de Persistencia

### Mapa de Transformación

```
sqlite3.IntegrityError
    ├─ UNIQUE constraint failed → SpaceAlreadyExistsException
    ├─ FOREIGN KEY constraint failed → (referencia inválida)
    └─ NOT NULL constraint failed → PersistenceException

sqlite3.OperationalError
    ├─ Table "X" already exists → PersistenceException
    ├─ No such table "X" → PersistenceException
    └─ Database disk image is malformed → PersistenceException

sqlite3.DatabaseError (base)
    └─ Otros errores → PersistenceException
```

### Código de Transformación

```python
try:
    # operación BD
except sqlite3.IntegrityError as e:
    if "UNIQUE constraint failed" in str(e):
        raise SpaceAlreadyExistsException(...)
    else:
        raise PersistenceException(...)
except sqlite3.OperationalError as e:
    raise PersistenceException(f"Database error: {e}")
```