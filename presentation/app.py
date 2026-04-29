"""Aplicación Flask para la API REST de SmartSpaces."""

from flask import Flask, request, jsonify
from datetime import datetime
from infrastructure.space_sqlite_repository import SpaceSQLiteRepository
from infrastructure.user_sqlite_repository import UserSQLiteRepository
from infrastructure.booking_sqlite_repository import BookingSQLiteRepository
from application.space_service import SpaceService
from application.user_service import UserService
from application.booking_service import BookingService
from domain.exceptions import (
    RepositoryException,
    UserNotFoundError,
    SpaceNotFoundError,
    BookingNotFoundError,
    UserAlreadyExistsException,
    SpaceAlreadyExistsException,
    BookingAlreadyExistsException,
    PersistenceException,
)
from domain.space_meetingroom import SpaceMeetingRoom

# ============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================================================

app = Flask(__name__)
DB_PATH = "smartspaces.db"

# Crear repositorios
space_repo = SpaceSQLiteRepository(DB_PATH)
user_repo = UserSQLiteRepository(DB_PATH)
booking_repo = BookingSQLiteRepository(DB_PATH)

# Crear servicios
user_service = UserService(user_repo)
space_service = SpaceService(space_repo, booking_repo)
booking_service = BookingService(booking_repo, space_repo, user_repo)

# ============================================================================
# UTILIDADES
# ============================================================================


def format_space(space):
    """Convierte un Space a diccionario para JSON."""
    data = {
        "space_id": space.space_id,
        "space_name": space.space_name,
        "capacity": space.capacity,
        "space_type": space.space_type,
        "space_status": space.space_status,
    }
    if isinstance(space, SpaceMeetingRoom):
        data.update(
            {
                "room_number": space.room_number,
                "floor": space.floor,
                "equipment_list": space.equipment_list,
                "num_power_outlets": space.num_power_outlets,
            }
        )
    return data


def format_user(user):
    """Convierte un User a diccionario para JSON."""
    return {
        "user_id": user.user_id,
        "name": user.name,
        "surname1": user.surname1,
        "surname2": user.surname2,
        "full_name": user.full_name(),
        "active": user.is_active(),
    }


def format_booking(booking):
    """Convierte un Booking a diccionario para JSON."""
    return {
        "booking_id": booking.booking_id,
        "space_id": booking.space.space_id,
        "space_name": booking.space.space_name,
        "user_id": booking.user.user_id,
        "user_name": booking.user.full_name(),
        "start_time": (
            booking.start_time.isoformat()
            if hasattr(booking.start_time, "isoformat")
            else str(booking.start_time)
        ),
        "end_time": (
            booking.end_time.isoformat()
            if hasattr(booking.end_time, "isoformat")
            else str(booking.end_time)
        ),
        "booking_status": booking.status,
    }


def error_response(message, code):
    """Devuelve una respuesta de error en JSON."""
    return jsonify({"error": message}), code


# ============================================================================
# RUTAS GENERALES
# ============================================================================


@app.route("/", methods=["GET"])
def index():
    """Bienvenida a la API."""
    return jsonify(
        {
            "app": "SmartSpaces API",
            "version": "1.0.0",
            "endpoints": {
                "users": "/users",
                "spaces": "/spaces",
                "bookings": "/bookings",
            },
        }
    )


@app.route("/health", methods=["GET"])
def health():
    """Verifica el estado de la API."""
    return jsonify({"status": "healthy"}), 200


# ============================================================================
# RUTAS DE USUARIOS
# ============================================================================


@app.route("/users", methods=["GET"])
def list_users():
    """GET /users - Lista todos los usuarios."""
    try:
        users = user_service.list_users()
        return jsonify([format_user(u) for u in users]), 200
    except Exception as e:
        return error_response(f"Error al listar usuarios: {str(e)}", 500)


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """GET /users/<user_id> - Obtiene un usuario por ID."""
    try:
        user = user_service.get_user(user_id)
        return jsonify(format_user(user)), 200
    except UserNotFoundError:
        return error_response(f"Usuario '{user_id}' no encontrado", 404)
    except Exception as e:
        return error_response(f"Error al obtener usuario: {str(e)}", 500)


@app.route("/users/nuevo/<user_id>/<name>/<surname1>/<surname2>", methods=["POST"])
def create_user_route(user_id, name, surname1, surname2):
    """POST /users/nuevo/<user_id>/<name>/<surname1>/<surname2> - Crea un usuario."""
    try:
        user = user_service.create_user(user_id, name, surname1, surname2)
        return jsonify(format_user(user)), 201
    except UserAlreadyExistsException:
        return error_response(f"Usuario con ID '{user_id}' ya existe", 409)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Error al crear usuario: {str(e)}", 500)


@app.route("/users/<user_id>/desactivar", methods=["POST"])
def deactivate_user_route(user_id):
    """POST /users/<user_id>/desactivar - Desactiva un usuario."""
    try:
        user = user_service.deactivate_user(user_id)
        return jsonify(format_user(user)), 200
    except UserNotFoundError:
        return error_response(f"Usuario '{user_id}' no encontrado", 404)
    except Exception as e:
        return error_response(f"Error al desactivar usuario: {str(e)}", 500)


# ============================================================================
# RUTAS DE ESPACIOS
# ============================================================================


@app.route("/spaces", methods=["GET"])
def list_spaces():
    """GET /spaces - Lista todos los espacios."""
    try:
        spaces = space_service.list_spaces()
        return jsonify([format_space(s) for s in spaces]), 200
    except Exception as e:
        return error_response(f"Error al listar espacios: {str(e)}", 500)


@app.route("/spaces/<space_id>", methods=["GET"])
def get_space(space_id):
    """GET /spaces/<space_id> - Obtiene un espacio por ID."""
    try:
        space = space_service.get_space(space_id)
        return jsonify(format_space(space)), 200
    except SpaceNotFoundError:
        return error_response(f"Espacio '{space_id}' no encontrado", 404)
    except Exception as e:
        return error_response(f"Error al obtener espacio: {str(e)}", 500)


@app.route("/spaces/nuevo/<space_name>/<int:capacity>/<space_type>", methods=["POST"])
def create_space_route(space_name, capacity, space_type):
    """POST /spaces/nuevo/<space_name>/<capacity>/<space_type> - Crea un espacio genérico."""
    try:
        space = space_service.create_space(space_name, capacity, space_type)
        return jsonify(format_space(space)), 201
    except SpaceAlreadyExistsException:
        return error_response(f"Espacio ya existe", 409)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Error al crear espacio: {str(e)}", 500)


@app.route(
    "/spaces/nueva-sala/<space_name>/<int:capacity>/<room_number>/<int:floor>/<int:num_power_outlets>",
    methods=["POST"],
)
def create_meeting_room_route(
    space_name, capacity, room_number, floor, num_power_outlets
):
    """POST /spaces/nueva-sala/... - Crea una sala de reuniones.

    Nota: equipment_list se pasa como parámetro JSON en el cuerpo de la solicitud.
    Ejemplo: {"equipment_list": ["Projector", "Whiteboard"]}
    """
    try:
        equipment_list = (
            request.get_json().get("equipment_list", []) if request.is_json else []
        )
        space = space_service.create_meeting_room(
            space_name, capacity, room_number, floor, num_power_outlets, equipment_list
        )
        return jsonify(format_space(space)), 201
    except SpaceAlreadyExistsException:
        return error_response(f"Sala ya existe", 409)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Error al crear sala: {str(e)}", 500)


@app.route("/spaces/disponibles/<fecha_inicio>/<fecha_fin>", methods=["GET"])
def get_available_spaces(fecha_inicio, fecha_fin):
    """GET /spaces/disponibles/<fecha_inicio>/<fecha_fin> - Espacios libres en el rango.

    Formato: ISO 8601, ej: 2026-04-25T09:00:00
    """
    try:
        start = datetime.fromisoformat(fecha_inicio)
        end = datetime.fromisoformat(fecha_fin)
        spaces = space_service.get_available_spaces(start, end)
        return jsonify([format_space(s) for s in spaces]), 200
    except ValueError:
        return error_response(
            f"Formato de fecha inválido. Use ISO 8601: YYYY-MM-DDTHH:MM:SS", 400
        )
    except Exception as e:
        return error_response(f"Error al buscar espacios disponibles: {str(e)}", 500)


# ============================================================================
# RUTAS DE RESERVAS
# ============================================================================


@app.route("/bookings", methods=["GET"])
def list_bookings():
    """GET /bookings - Lista todas las reservas."""
    try:
        bookings = booking_service.list_bookings()
        return jsonify([format_booking(b) for b in bookings]), 200
    except Exception as e:
        return error_response(f"Error al listar reservas: {str(e)}", 500)


@app.route("/bookings/<booking_id>", methods=["GET"])
def get_booking(booking_id):
    """GET /bookings/<booking_id> - Obtiene una reserva por ID."""
    try:
        booking = booking_service.get_booking(booking_id)
        return jsonify(format_booking(booking)), 200
    except BookingNotFoundError:
        return error_response(f"Reserva '{booking_id}' no encontrada", 404)
    except Exception as e:
        return error_response(f"Error al obtener reserva: {str(e)}", 500)


@app.route(
    "/bookings/nueva/<user_name>/<space_name>/<fecha_inicio>/<fecha_fin>",
    methods=["POST"],
)
def create_booking_route(user_name, space_name, fecha_inicio, fecha_fin):
    """POST /bookings/nueva/<user_name>/<space_name>/<fecha_inicio>/<fecha_fin> - Crea una reserva."""
    try:
        start = datetime.fromisoformat(fecha_inicio)
        end = datetime.fromisoformat(fecha_fin)
        booking = booking_service.create_booking(user_name, space_name, start, end)
        return jsonify(format_booking(booking)), 201
    except ValueError as e:
        if "ISO" in str(e):
            return error_response(
                f"Formato de fecha inválido. Use ISO 8601: YYYY-MM-DDTHH:MM:SS", 400
            )
        else:
            return error_response(str(e), 400)
    except BookingAlreadyExistsException:
        return error_response("Reserva ya existe", 409)
    except Exception as e:
        return error_response(f"Error al crear reserva: {str(e)}", 500)


@app.route("/bookings/<booking_id>/cancelar", methods=["POST"])
def cancel_booking_route(booking_id):
    """POST /bookings/<booking_id>/cancelar - Cancela una reserva."""
    try:
        booking = booking_service.cancel_booking(booking_id)
        return jsonify(format_booking(booking)), 200
    except BookingNotFoundError:
        return error_response(f"Reserva '{booking_id}' no encontrada", 404)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Error al cancelar reserva: {str(e)}", 500)


@app.route("/bookings/<booking_id>/finalizar", methods=["POST"])
def finish_booking_route(booking_id):
    """POST /bookings/<booking_id>/finalizar - Finaliza una reserva."""
    try:
        booking = booking_service.finish_booking(booking_id)
        return jsonify(format_booking(booking)), 200
    except BookingNotFoundError:
        return error_response(f"Reserva '{booking_id}' no encontrada", 404)
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Error al finalizar reserva: {str(e)}", 500)


@app.route(
    "/bookings/<booking_id>/reprogramar/<nueva_fecha_inicio>/<nueva_fecha_fin>",
    methods=["POST"],
)
def reschedule_booking_route(booking_id, nueva_fecha_inicio, nueva_fecha_fin):
    """POST /bookings/<booking_id>/reprogramar/... - Reprograma una reserva."""
    try:
        new_start = datetime.fromisoformat(nueva_fecha_inicio)
        new_end = datetime.fromisoformat(nueva_fecha_fin)
        booking = booking_service.modify_booking(booking_id, new_start, new_end)
        return jsonify(format_booking(booking)), 200
    except ValueError as e:
        if "ISO" in str(e):
            return error_response(
                f"Formato de fecha inválido. Use ISO 8601: YYYY-MM-DDTHH:MM:SS", 400
            )
        else:
            return error_response(str(e), 400)
    except BookingNotFoundError:
        return error_response(f"Reserva '{booking_id}' no encontrada", 404)
    except Exception as e:
        return error_response(f"Error al reprogramar reserva: {str(e)}", 500)


@app.route("/bookings/usuario/<user_name>", methods=["GET"])
def get_bookings_for_user_route(user_name):
    """GET /bookings/usuario/<user_name> - Reservas de un usuario."""
    try:
        bookings = booking_service.get_bookings_for_user(user_name)
        return jsonify([format_booking(b) for b in bookings]), 200
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(f"Error al obtener reservas: {str(e)}", 500)


@app.route("/bookings/espacio/<space_name>", methods=["GET"])
def get_bookings_for_space_route(space_name):
    """GET /bookings/espacio/<space_name> - Reservas de un espacio."""
    try:
        bookings = booking_service.get_bookings_for_space(space_name)
        return jsonify([format_booking(b) for b in bookings]), 200
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response(f"Error al obtener reservas: {str(e)}", 500)


# ============================================================================
# MANEJO GLOBAL DE ERRORES
# ============================================================================


@app.errorhandler(404)
def not_found(error):
    """Maneja rutas no encontradas."""
    return error_response("Ruta no encontrada", 404)


@app.errorhandler(500)
def internal_error(error):
    """Maneja errores internos del servidor."""
    return error_response("Error interno del servidor", 500)


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    print("🚀 Iniciando SmartSpaces API...")
    print("📌 Base de datos: smartspaces.db")
    print("🌐 Servidor: http://localhost:5000")
    print("📚 Documentación disponible en: /")
    app.run(debug=True, host="0.0.0.0", port=5000)
