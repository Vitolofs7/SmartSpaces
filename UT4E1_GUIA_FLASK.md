# Guía de rutas Flask — SmartSpaces API

> **Actividad**: ut4e1 — Exposición de la API REST completa del dominio SmartSpaces como routes Flask  
> **Alumno**: Victor  
> **Fecha**: 2026-04-24  
> **Versión del proyecto base**: 0.4.1

---

## 1. Inventario completo del menú actual

La aplicación consola (`presentation/menu.py`) expone las siguientes opciones:

| # | Opción | Servicio invocado | Método |
|---|--------|-------------------|--------|
| 1 | List spaces | `SpaceService` | `list_spaces()` |
| 2 | List users | `UserService` | `list_users()` |
| 3 | List bookings | `BookingService` | `list_bookings()` |
| 4 | Create booking | `BookingService` | `create_booking(user_name, space_name, start_time, end_time)` |
| 5 | Cancel booking | `BookingService` | `cancel_booking(booking_id)` |
| 6 | Finish booking | `BookingService` | `finish_booking(booking_id)` |
| 7 | Create space | `SpaceService` | `create_space(space_name, capacity, space_type)` / `create_meeting_room(space_name, capacity, room_number, floor, num_power_outlets, equipment_list)` |
| 8 | List available spaces | `SpaceService` | `get_available_spaces(start, end)` |
| 9 | Modify booking | `BookingService` | `modify_booking(booking_id, new_start, new_end)` |
| 10 | Exit | — | — |

---

## 2. Rutas sugeridas (toda la API)

Los parámetros de creación/modificación se pasan como segmentos de URL.

### Usuarios

| Ruta Flask | Método del servicio | Descripción |
|------------|---------------------|-------------|
| `/users` | `user_service.list_users()` | Lista todos los usuarios |
| `/users/<user_id>` | `user_service.get_user(user_id)` | Obtiene un usuario por ID |
| `/users/nuevo/<user_id>/<nombre>/<apellido1>/<apellido2>` | `user_service.create_user(user_id, nombre, apellido1, apellido2)` | Crea un nuevo usuario |
| `/users/<user_id>/desactivar` | `user_service.deactivate_user(user_id)` | Desactiva un usuario |

---

### Espacios

| Ruta Flask | Método del servicio | Descripción |
|------------|---------------------|-------------|
| `/spaces` | `space_service.list_spaces()` | Lista todos los espacios |
| `/spaces/<space_id>` | `space_service.get_space(space_id)` | Obtiene un espacio por ID |
| `/spaces/nuevo/<space_name>/<capacity>/<space_type>` | `space_service.create_space(space_name, capacity, space_type)` | Crea un espacio genérico |
| `/spaces/nueva-sala/<space_name>/<capacity>/<room_number>/<floor>/<num_power_outlets>` | `space_service.create_meeting_room(space_name, capacity, room_number, floor, num_power_outlets, [])` | Crea una sala de reuniones (`SpaceMeetingRoom`) |
| `/spaces/disponibles/<fecha_inicio>/<fecha_fin>` | `space_service.get_available_spaces(fecha_inicio, fecha_fin)` | Espacios libres en el rango indicado |

> `fecha_inicio` y `fecha_fin` se pasan en formato ISO 8601, por ejemplo `2026-04-25T09:00`.

---

### Reservas

| Ruta Flask | Método del servicio | Descripción |
|------------|---------------------|-------------|
| `/bookings` | `booking_service.list_bookings()` | Lista todas las reservas |
| `/bookings/<booking_id>` | `booking_service.get_booking(booking_id)` | Obtiene una reserva por ID |
| `/bookings/nueva/<user_name>/<space_name>/<fecha_inicio>/<fecha_fin>` | `booking_service.create_booking(user_name, space_name, fecha_inicio, fecha_fin)` | Crea una nueva reserva |
| `/bookings/<booking_id>/cancelar` | `booking_service.cancel_booking(booking_id)` | Cancela una reserva activa |
| `/bookings/<booking_id>/finalizar` | `booking_service.finish_booking(booking_id)` | Finaliza una reserva activa |
| `/bookings/<booking_id>/reprogramar/<nueva_fecha_inicio>/<nueva_fecha_fin>` | `booking_service.modify_booking(booking_id, nueva_fecha_inicio, nueva_fecha_fin)` | Reprograma una reserva activa |
| `/bookings/usuario/<user_name>` | `booking_service.get_bookings_for_user(user_name)` | Reservas de un usuario concreto |
| `/bookings/espacio/<space_name>` | `booking_service.get_bookings_for_space(space_name)` | Reservas de un espacio concreto |

### Ejemplo: cómo quedaría `app.py` con dos rutas ya hechas

El siguiente fragmento muestra la estructura mínima de `app.py` con dos rutas implementadas
para que puedas tomar el patrón y aplicarlo al resto:

```python
from flask import Flask
from infrastructure.space_sqlite_repository import SpaceSQLiteRepository
from infrastructure.user_sqlite_repository import UserSQLiteRepository
from infrastructure.booking_sqlite_repository import BookingSQLiteRepository
from application.space_service import SpaceService
from application.user_service import UserService
from application.booking_service import BookingService

app = Flask(__name__)

DB_PATH = "smartspaces.db"
space_repo = SpaceSQLiteRepository(DB_PATH)
user_repo = UserSQLiteRepository(DB_PATH)
booking_repo = BookingSQLiteRepository(DB_PATH)
user_service = UserService(user_repo)
space_service = SpaceService(space_repo, booking_repo)
booking_service = BookingService(booking_repo, space_repo, user_repo)


@app.route("/")
def bienvenida():
    return (
        "Bienvenido a SmartSpaces\n"
        "  /users    → lista de usuarios\n"
        "  /spaces   → lista de espacios\n"
        "  /bookings → lista de reservas\n"
    )


@app.route("/spaces")
def listar_espacios():
    espacios = space_service.list_spaces()
    if not espacios:
        return "No hay espacios registrados."
    return "\n".join(str(e) for e in espacios)


if __name__ == "__main__":
    app.run(debug=True)
```

**Lo que hace cada parte:**

- El repositorio y el servicio se crean **una sola vez** fuera de las vistas, al arrancar la
  aplicación. Así todas las rutas comparten el mismo acceso a la base de datos SQLite.
- Cada función de vista llama al método del servicio correspondiente y devuelve texto plano.
- Para rutas con `ValueError` puedes devolver una tupla `(mensaje, código)`:
  `return "No encontrado", 404` o `return "Ya existe", 409`.

---

## 3. Métodos de servicio a añadir

Los métodos indicados a continuación no existen actualmente; es necesario implementarlos para poder exponer las rutas de detalle y administración de usuarios y espacios.

### `UserService`

| Método nuevo | Descripción | Excepción esperada |
|---|---|---|
| `get_user(user_id: str)` | Recupera un usuario por su ID desde `_user_repo.get(user_id)` | `UserNotFoundError` → 404 |
| `create_user(user_id, name, surname1, surname2)` | Instancia `User` y lo persiste con `_user_repo.save(user)` | `UserAlreadyExistsException` → 409 |
| `deactivate_user(user_id: str)` | Recupera el usuario, llama a `user.deactivate()` y persiste con `_user_repo.update(user)` | `UserNotFoundError` → 404 |

### `SpaceService`

| Método nuevo | Descripción | Excepción esperada |
|---|---|---|
| `get_space(space_id: str)` | Recupera un espacio por su ID desde `_space_repo.get(space_id)` | `SpaceNotFoundError` → 404 |

> Nota: la infraestructura SQLite (`SpaceSQLiteRepository`, `UserSQLiteRepository`) ya implementa `get()`, `update()`, y `delete()` en el contrato del repositorio; solo falta el método en la capa de servicio.

---

## 4. Mapa de excepciones → códigos HTTP

| Excepción del dominio | Situación | Código HTTP |
|---|---|---|
| `ValueError("User not found")` | Usuario no encontrado por nombre en `create_booking` | 404 Not Found |
| `ValueError("Space not found")` | Espacio no encontrado por nombre | 404 Not Found |
| `UserNotFoundError` | ID de usuario no existe en repositorio | 404 Not Found |
| `SpaceNotFoundError` | ID de espacio no existe | 404 Not Found |
| `BookingNotFoundError` | ID de reserva no existe | 404 Not Found |
| `UserAlreadyExistsException` | Crear usuario con ID duplicado | 409 Conflict |
| `SpaceAlreadyExistsException` | Crear espacio con ID duplicado | 409 Conflict |
| `BookingAlreadyExistsException` | Reserva duplicada | 409 Conflict |
| `ValueError("Space '...' already booked.")` | Reserva solapada con una activa | 409 Conflict |
| `ValueError("User '...' has reached the maximum...")` | Límite `max_active_bookings` alcanzado | 409 Conflict |
| `ValueError("Booking duration exceeds...")` | Supera `max_booking_duration` | 400 Bad Request |
| `ValueError("User is inactive")` | Reserva para usuario inactivo | 400 Bad Request |
| `ValueError("Space is under maintenance...")` | Espacio en mantenimiento | 400 Bad Request |
| `ValueError("Only active bookings can be cancelled")` | Cancelar reserva ya finalizada/cancelada | 400 Bad Request |
| `ValueError("Only active bookings can be finished")` | Finalizar reserva ya finalizada/cancelada | 400 Bad Request |
| `PersistenceException` | Error inesperado de base de datos | 500 Internal Server Error |

---

## 5. Advertencias

### 5.1 Reservas solapadas → 409 Conflict

`Booking.create()` lanza `ValueError("Space '...' already booked.")` cuando la nueva reserva se solapa en tiempo con otra reserva **activa** del mismo espacio. En la route Flask, capturar ese `ValueError` y devolver `409`.

Un espacio con estado `RESERVED` **puede** aceptar nuevas reservas en franjas horarias que no solapen — no confundir estado del espacio con disponibilidad real.

### 5.2 Validación de límites por usuario

`BookingService.create_booking` aplica dos reglas del dominio antes de delegar en `Booking.create`:

- `max_active_bookings = 1` (valor por defecto en `User`): un usuario no puede tener más de una reserva activa simultánea. Si se supera → `ValueError` → **409 Conflict**.
- `max_booking_duration = timedelta(hours=2)` (valor por defecto en `User`): la duración de la reserva no puede superar 2 horas. Si se supera → `ValueError` → **400 Bad Request**.

### 5.3 `SpaceMeetingRoom` como subtipo de `Space`

`SpaceMeetingRoom` hereda de `Space` y añade los atributos `room_number`, `floor`, `num_power_outlets` y `equipment_list`. Al mostrar un espacio en el route Flask, usa `isinstance(space, SpaceMeetingRoom)` para saber si debes incluir los campos extra del subtipo en el texto de respuesta.

### 5.4 Estados de reserva (`booking_status`)

`Booking` maneja tres estados: `ACTIVE`, `CANCELLED`, `FINISHED`. Solo las reservas activas pueden cancelarse o finalizarse; intentar hacerlo en otro estado lanza `ValueError` → **400**.

### 5.5 Usuarios activos/inactivos

`User.is_active()` determina si el usuario puede realizar reservas. `Booking.create` lo comprueba internamente y lanza `ValueError("User is inactive")` si el usuario está desactivado → **400**.

### 5.6 Fechas como texto

Los datetimes se almacenan en SQLite como texto ISO 8601. Al recibir fechas en la route Flask (como segmentos de URL), parsearlas con `datetime.fromisoformat()` antes de pasarlas al servicio. Al devolver fechas en la respuesta, convertirlas a texto con `str(booking.start_time)` o `.isoformat()`.
