"""
SmartSpaces REST API - Versión con Jinja2 templates (Lab A4 patrones)
Actividad UT4E3: Plantillas base, herencia, y renderizado dinámico
"""

import logging
from flask import Flask, request, jsonify, redirect, url_for, render_template
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
# CONFIGURACIÓN DE LOGGING
# ============================================================================

logging.basicConfig(
    filename='smartspaces.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
logger.info("=" * 80)
logger.info("SmartSpaces API iniciada (UT4E3 - Templates)")
logger.info("=" * 80)

# ============================================================================
# CONFIGURACIÓN DE FLASK
# ============================================================================

app = Flask(__name__)
DB_PATH = "smartspaces.db"

# Crear repositorios
space_repo = SpaceSQLiteRepository(DB_PATH)
user_repo = UserSQLiteRepository(DB_PATH)
booking_repo = BookingSQLiteRepository(DB_PATH)

# Crear servicios - Bootstrap
user_service = UserService(user_repo)
space_service = SpaceService(space_repo, booking_repo)
booking_service = BookingService(booking_repo, space_repo, user_repo)

# ============================================================================
# HOOK: Logging de peticiones
# ============================================================================

@app.before_request
def log_request():
    """Registra cada petición: método y ruta."""
    logger.info(f"{request.method} {request.path}")

# ============================================================================
# FUNCIONES AUXILIARES (Serialización)
# ============================================================================

def format_space(space):
    """Convierte un Space a diccionario para JSON o plantilla."""
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
    """Convierte un User a diccionario para JSON o plantilla."""
    return {
        "user_id": user.user_id,
        "name": user.name,
        "surname1": user.surname1,
        "surname2": user.surname2,
        "full_name": user.full_name(),
        "active": user.is_active(),
    }


def format_booking(booking):
    """Convierte un Booking a diccionario para JSON o plantilla."""
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
# MANEJADORES GLOBALES DE ERROR
# ============================================================================

@app.errorhandler(404)
def error_404(error):
    """Manejador de errores 404 - Ruta no encontrada."""
    logger.warning(f"404 Not Found: {request.method} {request.path}")
    return render_template('error.html', code=404, path=request.path), 404


@app.errorhandler(500)
def error_500(error):
    """Manejador de errores 500 - Error interno del servidor."""
    logger.error(f"500 Internal Server Error: {request.method} {request.path} - {str(error)}")
    return render_template('error.html', code=500), 500

# ============================================================================
# RUTA AYUDA (Plantilla)
# ============================================================================

@app.route("/ayuda")
def ayuda():
    """Ruta /ayuda que lista todas las rutas registradas."""
    routes = []
    
    # Iterar todas las rutas registradas
    for rule in app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue
        
        methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
        route_path = str(rule)
        endpoint = rule.endpoint
        
        routes.append({
            'path': route_path,
            'methods': methods,
            'endpoint': endpoint
        })
    
    routes.sort(key=lambda x: x['path'])
    logger.info(f"Acceso a /ayuda - Mostrando {len(routes)} rutas")
    
    return render_template('ayuda.html', routes=routes)

# ============================================================================
# RUTA INICIAL (Plantilla)
# ============================================================================

@app.route("/")
def index():
    """Página de inicio."""
    return render_template('index.html')

# ============================================================================
# USUARIOS - LECTURA (Plantillas)
# ============================================================================

@app.route("/users", methods=["GET"])
def list_users():
    """GET /users - Lista todos los usuarios."""
    try:
        users = user_service.list_users()
        formatted_users = [format_user(u) for u in users]
        return render_template('users.html', users=formatted_users)
    except Exception as e:
        logger.error(f"Error al listar usuarios: {str(e)}")
        return error_response(f"Error al listar usuarios: {str(e)}", 500)


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """GET /users/<user_id> - Obtiene un usuario por ID."""
    try:
        user = user_service.get_user(user_id)
        formatted_user = format_user(user)
        return render_template('user_detail.html', user=formatted_user)
    except UserNotFoundError:
        logger.warning(f"Usuario no encontrado: {user_id}")
        return render_template('error.html', code=404, path=f"/users/{user_id}"), 404
    except Exception as e:
        logger.error(f"Error al obtener usuario {user_id}: {str(e)}")
        return error_response(f"Error al obtener usuario: {str(e)}", 500)

# ============================================================================
# ESPACIOS - LECTURA (Plantillas)
# ============================================================================

@app.route("/spaces", methods=["GET"])
def list_spaces():
    """GET /spaces - Lista todos los espacios."""
    try:
        spaces = space_service.list_spaces()
        formatted_spaces = [format_space(s) for s in spaces]
        return render_template('spaces.html', spaces=formatted_spaces)
    except Exception as e:
        logger.error(f"Error al listar espacios: {str(e)}")
        return error_response(f"Error al listar espacios: {str(e)}", 500)


@app.route("/spaces/<space_id>", methods=["GET"])
def get_space(space_id):
    """GET /spaces/<space_id> - Obtiene un espacio por ID."""
    try:
        space = space_service.get_space(space_id)
        formatted_space = format_space(space)
        return render_template('space_detail.html', space=formatted_space)
    except SpaceNotFoundError:
        logger.warning(f"Espacio no encontrado: {space_id}")
        return render_template('error.html', code=404, path=f"/spaces/{space_id}"), 404
    except Exception as e:
        logger.error(f"Error al obtener espacio {space_id}: {str(e)}")
        return error_response(f"Error al obtener espacio: {str(e)}", 500)

# ============================================================================
# RESERVAS - LECTURA (Plantillas)
# ============================================================================

@app.route("/bookings", methods=["GET"])
def list_bookings():
    """GET /bookings - Lista todas las reservas."""
    try:
        bookings = booking_service.list_bookings()
        formatted_bookings = [format_booking(b) for b in bookings]
        return render_template('bookings.html', bookings=formatted_bookings)
    except Exception as e:
        logger.error(f"Error al listar reservas: {str(e)}")
        return error_response(f"Error al listar reservas: {str(e)}", 500)


@app.route("/bookings/<booking_id>", methods=["GET"])
def get_booking(booking_id):
    """GET /bookings/<booking_id> - Obtiene una reserva por ID."""
    try:
        booking = booking_service.get_booking(booking_id)
        formatted_booking = format_booking(booking)
        return render_template('booking_detail.html', booking=formatted_booking)
    except BookingNotFoundError:
        logger.warning(f"Reserva no encontrada: {booking_id}")
        return render_template('error.html', code=404, path=f"/bookings/{booking_id}"), 404
    except Exception as e:
        logger.error(f"Error al obtener reserva {booking_id}: {str(e)}")
        return error_response(f"Error al obtener reserva: {str(e)}", 500)


@app.route("/spaces/disponibles/<fecha_inicio>/<fecha_fin>", methods=["GET"])
def get_available_spaces(fecha_inicio, fecha_fin):
    """GET /spaces/disponibles/<fecha_inicio>/<fecha_fin> - Espacios libres en rango."""
    try:
        start = datetime.fromisoformat(fecha_inicio)
        end = datetime.fromisoformat(fecha_fin)
        spaces = space_service.get_available_spaces(start, end)
        formatted_spaces = [format_space(s) for s in spaces]
        return render_template('spaces.html', spaces=formatted_spaces)
    except ValueError:
        logger.warning(f"Formato de fecha inválido: {fecha_inicio}/{fecha_fin}")
        return error_response(
            f"Formato de fecha inválido. Use ISO 8601: YYYY-MM-DDTHH:MM:SS", 400
        )
    except Exception as e:
        logger.error(f"Error al buscar espacios disponibles: {str(e)}")
        return error_response(f"Error al buscar espacios disponibles: {str(e)}", 500)

# ============================================================================
# CREACIÓN DE USUARIOS (POST con redirect)
# ============================================================================

@app.route("/users/nuevo/<user_id>/<name>/<surname1>/<surname2>", methods=["POST"])
def create_user_route(user_id, name, surname1, surname2):
    """POST /users/nuevo/<user_id>/<name>/<surname1>/<surname2> - Crea un usuario."""
    try:
        user = user_service.create_user(user_id, name, surname1, surname2)
        logger.info(f"Usuario creado: {user_id}")
        return redirect(url_for("get_user", user_id=user_id))
    except UserAlreadyExistsException:
        logger.warning(f"Intento de crear usuario duplicado: {user_id}")
        return error_response(f"Usuario con ID '{user_id}' ya existe", 409)
    except ValueError as e:
        logger.warning(f"Datos inválidos al crear usuario: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error al crear usuario: {str(e)}")
        return error_response(f"Error al crear usuario: {str(e)}", 500)

# ============================================================================
# CREACIÓN DE ESPACIOS (POST con redirect)
# ============================================================================

@app.route("/spaces/nuevo/<space_name>/<int:capacity>/<space_type>", methods=["POST"])
def create_space_route(space_name, capacity, space_type):
    """POST /spaces/nuevo/<space_name>/<capacity>/<space_type> - Crea un espacio."""
    try:
        space = space_service.create_space(space_name, capacity, space_type)
        logger.info(f"Espacio creado: {space.space_id}")
        return redirect(url_for("get_space", space_id=space.space_id))
    except SpaceAlreadyExistsException:
        logger.warning(f"Intento de crear espacio duplicado")
        return error_response(f"Espacio ya existe", 409)
    except ValueError as e:
        logger.warning(f"Datos inválidos al crear espacio: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error al crear espacio: {str(e)}")
        return error_response(f"Error al crear espacio: {str(e)}", 500)

# ============================================================================
# CREACIÓN DE RESERVAS (POST con redirect)
# ============================================================================

@app.route(
    "/bookings/nueva/<user_name>/<space_name>/<fecha_inicio>/<fecha_fin>",
    methods=["POST"],
)
def create_booking_route(user_name, space_name, fecha_inicio, fecha_fin):
    """POST /bookings/nueva/... - Crea una reserva."""
    try:
        start = datetime.fromisoformat(fecha_inicio)
        end = datetime.fromisoformat(fecha_fin)
        booking = booking_service.create_booking(user_name, space_name, start, end)
        logger.info(f"Reserva creada: {booking.booking_id}")
        return redirect(url_for("get_booking", booking_id=booking.booking_id))
    except ValueError as e:
        if "ISO" in str(e):
            logger.warning(f"Formato de fecha inválido: {fecha_inicio}/{fecha_fin}")
            return error_response(
                f"Formato de fecha inválido. Use ISO 8601: YYYY-MM-DDTHH:MM:SS", 400
            )
        else:
            logger.warning(f"Datos inválidos al crear reserva: {str(e)}")
            return error_response(str(e), 400)
    except BookingAlreadyExistsException:
        logger.warning(f"Intento de crear reserva duplicada")
        return error_response("Reserva ya existe", 409)
    except Exception as e:
        logger.error(f"Error al crear reserva: {str(e)}")
        return error_response(f"Error al crear reserva: {str(e)}", 500)

# ============================================================================
# CAMBIOS DE ESTADO (POST con redirect)
# ============================================================================

@app.route("/bookings/<booking_id>/cancelar", methods=["POST"])
def cancel_booking_route(booking_id):
    """POST /bookings/<booking_id>/cancelar - Cancela una reserva."""
    try:
        booking = booking_service.cancel_booking(booking_id)
        logger.info(f"Reserva cancelada: {booking_id}")
        return redirect(url_for("get_booking", booking_id=booking_id))
    except BookingNotFoundError:
        logger.warning(f"Intento de cancelar reserva inexistente: {booking_id}")
        return error_response(f"Reserva '{booking_id}' no encontrada", 404)
    except ValueError as e:
        logger.warning(f"Error al cancelar reserva: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error al cancelar reserva: {str(e)}")
        return error_response(f"Error al cancelar reserva: {str(e)}", 500)


@app.route("/bookings/<booking_id>/finalizar", methods=["POST"])
def finish_booking_route(booking_id):
    """POST /bookings/<booking_id>/finalizar - Finaliza una reserva."""
    try:
        booking = booking_service.finish_booking(booking_id)
        logger.info(f"Reserva finalizada: {booking_id}")
        return redirect(url_for("get_booking", booking_id=booking_id))
    except BookingNotFoundError:
        logger.warning(f"Intento de finalizar reserva inexistente: {booking_id}")
        return error_response(f"Reserva '{booking_id}' no encontrada", 404)
    except ValueError as e:
        logger.warning(f"Error al finalizar reserva: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error al finalizar reserva: {str(e)}")
        return error_response(f"Error al finalizar reserva: {str(e)}", 500)

# ============================================================================
# DESACTIVACIONES (POST con redirect)
# ============================================================================

@app.route("/users/<user_id>/desactivar", methods=["POST"])
def deactivate_user_route(user_id):
    """POST /users/<user_id>/desactivar - Desactiva un usuario."""
    try:
        user = user_service.deactivate_user(user_id)
        logger.info(f"Usuario desactivado: {user_id}")
        return redirect(url_for("get_user", user_id=user_id))
    except UserNotFoundError:
        logger.warning(f"Intento de desactivar usuario inexistente: {user_id}")
        return error_response(f"Usuario '{user_id}' no encontrado", 404)
    except Exception as e:
        logger.error(f"Error al desactivar usuario: {str(e)}")
        return error_response(f"Error al desactivar usuario: {str(e)}", 500)

# ============================================================================
# CREACIÓN DE SALAS DE REUNIONES (POST con redirect)
# ============================================================================

@app.route(
    "/spaces/nueva-sala/<space_name>/<int:capacity>/<room_number>/<int:floor>/<int:num_power_outlets>",
    methods=["POST"],
)
def create_meeting_room_route(
    space_name, capacity, room_number, floor, num_power_outlets
):
    """POST /spaces/nueva-sala/... - Crea una sala de reuniones."""
    try:
        equipment_list = (
            request.get_json().get("equipment_list", []) if request.is_json else []
        )
        space = space_service.create_meeting_room(
            space_name, capacity, room_number, floor, num_power_outlets, equipment_list
        )
        logger.info(f"Sala de reuniones creada: {space.space_id}")
        return redirect(url_for("get_space", space_id=space.space_id))
    except SpaceAlreadyExistsException:
        logger.warning(f"Intento de crear sala duplicada")
        return error_response(f"Sala ya existe", 409)
    except ValueError as e:
        logger.warning(f"Datos inválidos al crear sala: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        logger.error(f"Error al crear sala: {str(e)}")
        return error_response(f"Error al crear sala: {str(e)}", 500)

# ============================================================================
# REPROGRAMACIÓN DE RESERVAS (POST con redirect)
# ============================================================================

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
        logger.info(f"Reserva reprogramada: {booking_id}")
        return redirect(url_for("get_booking", booking_id=booking_id))
    except ValueError as e:
        if "ISO" in str(e):
            logger.warning(f"Formato de fecha inválido: {nueva_fecha_inicio}/{nueva_fecha_fin}")
            return error_response(
                f"Formato de fecha inválido. Use ISO 8601: YYYY-MM-DDTHH:MM:SS", 400
            )
        else:
            logger.warning(f"Error al reprogramar reserva: {str(e)}")
            return error_response(str(e), 400)
    except BookingNotFoundError:
        logger.warning(f"Intento de reprogramar reserva inexistente: {booking_id}")
        return error_response(f"Reserva '{booking_id}' no encontrada", 404)
    except Exception as e:
        logger.error(f"Error al reprogramar reserva: {str(e)}")
        return error_response(f"Error al reprogramar reserva: {str(e)}", 500)

# ============================================================================
# BÚSQUEDAS POR USUARIO Y ESPACIO (GET - Plantillas)
# ============================================================================

@app.route("/bookings/usuario/<user_name>", methods=["GET"])
def get_bookings_for_user_route(user_name):
    """GET /bookings/usuario/<user_name> - Reservas de un usuario."""
    try:
        bookings = booking_service.get_bookings_for_user(user_name)
        formatted_bookings = [format_booking(b) for b in bookings]
        return render_template('bookings.html', bookings=formatted_bookings)
    except ValueError as e:
        logger.warning(f"Usuario no encontrado: {user_name}")
        return render_template('error.html', code=404, path=f"/bookings/usuario/{user_name}"), 404
    except Exception as e:
        logger.error(f"Error al obtener reservas: {str(e)}")
        return error_response(f"Error al obtener reservas: {str(e)}", 500)


@app.route("/bookings/espacio/<space_name>", methods=["GET"])
def get_bookings_for_space_route(space_name):
    """GET /bookings/espacio/<space_name> - Reservas de un espacio."""
    try:
        bookings = booking_service.get_bookings_for_space(space_name)
        formatted_bookings = [format_booking(b) for b in bookings]
        return render_template('bookings.html', bookings=formatted_bookings)
    except ValueError as e:
        logger.warning(f"Espacio no encontrado: {space_name}")
        return render_template('error.html', code=404, path=f"/bookings/espacio/{space_name}"), 404
    except Exception as e:
        logger.error(f"Error al obtener reservas: {str(e)}")
        return error_response(f"Error al obtener reservas: {str(e)}", 500)

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 Iniciando SmartSpaces API (UT4E3 - Templates)...")
    print("📌 Base de datos: smartspaces.db")
    print("📊 Logging: smartspaces.log")
    print("🌐 Servidor: http://localhost:5000")
    print("📚 Ayuda: http://localhost:5000/ayuda")
    print("🎨 Templates: presentation/templates/")
    print("=" * 80)
    logger.info("Iniciando servidor Flask con templates")
    app.run(debug=True, host="0.0.0.0", port=5000)