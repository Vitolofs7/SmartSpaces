import logging
from flask import Flask, request, jsonify, redirect, url_for
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
# CONFIGURACIÓN DE LOGGING (Patrón 4 - Lab A3)
# ============================================================================

logging.basicConfig(
    filename='smartspaces.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
logger.info("=" * 80)
logger.info("SmartSpaces API iniciada")
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
# HOOK: Logging de peticiones (Patrón 3 - Lab A3)
# ============================================================================

@app.before_request
def log_request():
    """Registra cada petición: método y ruta."""
    logger.info(f"{request.method} {request.path}")


# ============================================================================
# FUNCIONES AUXILIARES (Serialización)
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
# MANEJADORES GLOBALES DE ERROR (Patrones 1 y 2 - Lab A3)
# ============================================================================

@app.errorhandler(404)
def error_404(error):
    """Manejador de errores 404 - Ruta no encontrada.
    
    Devuelve HTML personalizado con mensaje amigable.
    """
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error 404 - No encontrado</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                border-left: 4px solid #e74c3c;
            }
            h1 {
                color: #e74c3c;
                margin-top: 0;
            }
            p {
                color: #555;
                line-height: 1.6;
            }
            .path {
                background-color: #f9f9f9;
                padding: 10px;
                border-radius: 4px;
                font-family: monospace;
                margin: 15px 0;
                word-break: break-all;
            }
            .links {
                margin-top: 20px;
                border-top: 1px solid #eee;
                padding-top: 20px;
            }
            a {
                color: #3498db;
                text-decoration: none;
                margin-right: 15px;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>❌ Error 404 - Ruta no encontrada</h1>
            <p>La ruta que intentas acceder no existe en esta API.</p>
            <div class="path">{}</div>
            <div class="links">
                <p><strong>Rutas disponibles:</strong></p>
                <a href="/">Inicio</a>
                <a href="/ayuda">Ver todas las rutas</a>
            </div>
        </div>
    </body>
    </html>
    """.format(request.path)
    
    logger.warning(f"404 Not Found: {request.method} {request.path}")
    return html, 404


@app.errorhandler(500)
def error_500(error):
    """Manejador de errores 500 - Error interno del servidor.
    
    Devuelve HTML personalizado con mensaje amigable.
    """
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Error 500 - Error interno</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                border-left: 4px solid #c0392b;
            }
            h1 {
                color: #c0392b;
                margin-top: 0;
            }
            p {
                color: #555;
                line-height: 1.6;
            }
            .error-details {
                background-color: #ffe6e6;
                padding: 15px;
                border-radius: 4px;
                margin: 15px 0;
                color: #a93226;
                font-family: monospace;
                font-size: 13px;
                word-break: break-all;
            }
            .links {
                margin-top: 20px;
                border-top: 1px solid #eee;
                padding-top: 20px;
            }
            a {
                color: #3498db;
                text-decoration: none;
                margin-right: 15px;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚠️ Error 500 - Error interno del servidor</h1>
            <p>Algo ha salido mal en el servidor. El equipo técnico ha sido notificado.</p>
            <div class="error-details">
                Por favor, intenta más tarde o contacta con el administrador.
            </div>
            <div class="links">
                <p><strong>Acciones disponibles:</strong></p>
                <a href="/">Volver al inicio</a>
                <a href="/ayuda">Ver rutas disponibles</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    logger.error(f"500 Internal Server Error: {request.method} {request.path} - {str(error)}")
    return html, 500

# ============================================================================
# RUTA AYUDA (Patrón 2 - Lab A3)
# ============================================================================

@app.route("/ayuda")
def ayuda():
    """Ruta /ayuda que lista todas las rutas registradas en la API.
    
    Itera app.url_map.iter_rules() y construye HTML con la lista.
    Se autoactualiza: al añadir/quitar rutas, /ayuda refleja los cambios.
    """
    routes = []
    
    # Iterar todas las rutas registradas
    for rule in app.url_map.iter_rules():
        # Filtrar rutas static (generadas automáticamente por Flask)
        if rule.endpoint == 'static':
            continue
        
        # Extraer información de la ruta
        methods = ','.join(sorted(rule.methods - {'OPTIONS', 'HEAD'}))
        route_path = str(rule)
        endpoint = rule.endpoint
        
        routes.append({
            'path': route_path,
            'methods': methods,
            'endpoint': endpoint
        })
    
    # Ordenar por ruta
    routes.sort(key=lambda x: x['path'])
    
    # Construir tabla HTML
    rows_html = ""
    for route in routes:
        rows_html += f"""
        <tr>
            <td><code>{route['path']}</code></td>
            <td>{route['methods']}</td>
            <td>{route['endpoint']}</td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SmartSpaces API - Ayuda</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 1000px;
                margin: 20px auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #2c3e50;
                margin-top: 0;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
            }}
            p {{
                color: #555;
                line-height: 1.6;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th {{
                background-color: #3498db;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: bold;
            }}
            td {{
                padding: 10px 12px;
                border-bottom: 1px solid #ddd;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tr:hover {{
                background-color: #f0f0f0;
            }}
            code {{
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: monospace;
            }}
            .method {{
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
            }}
            .method.get {{
                background-color: #d4edda;
                color: #155724;
            }}
            .method.post {{
                background-color: #cfe2ff;
                color: #084298;
            }}
            .back-link {{
                margin-top: 20px;
                text-align: center;
            }}
            a {{
                color: #3498db;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 SmartSpaces API - Ayuda</h1>
            
            <h2>Rutas registradas ({len(routes)} endpoints)</h2>
            <p>Esta tabla se autoactualiza automáticamente al añadir o eliminar rutas.</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Ruta</th>
                        <th>Métodos HTTP</th>
                        <th>Función</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
            
            <div class="back-link">
                <a href="/">← Volver al inicio</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    logger.info(f"Acceso a /ayuda - Mostrando {len(routes)} rutas")
    return html, 200

# ============================================================================
# RUTA INICIAL
# ============================================================================

@app.route("/")
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
                "ayuda": "/ayuda",
            },
        }
    )

# ============================================================================
# USUARIOS - LECTURA
# ============================================================================

@app.route("/users", methods=["GET"])
def list_users():
    """GET /users - Lista todos los usuarios."""
    try:
        users = user_service.list_users()
        return jsonify([format_user(u) for u in users]), 200
    except Exception as e:
        logger.error(f"Error al listar usuarios: {str(e)}")
        return error_response(f"Error al listar usuarios: {str(e)}", 500)


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """GET /users/<user_id> - Obtiene un usuario por ID."""
    try:
        user = user_service.get_user(user_id)
        return jsonify(format_user(user)), 200
    except UserNotFoundError:
        logger.warning(f"Usuario no encontrado: {user_id}")
        return error_response(f"Usuario '{user_id}' no encontrado", 404)
    except Exception as e:
        logger.error(f"Error al obtener usuario {user_id}: {str(e)}")
        return error_response(f"Error al obtener usuario: {str(e)}", 500)

# ============================================================================
# ESPACIOS - LECTURA
# ============================================================================

@app.route("/spaces", methods=["GET"])
def list_spaces():
    """GET /spaces - Lista todos los espacios."""
    try:
        spaces = space_service.list_spaces()
        return jsonify([format_space(s) for s in spaces]), 200
    except Exception as e:
        logger.error(f"Error al listar espacios: {str(e)}")
        return error_response(f"Error al listar espacios: {str(e)}", 500)


@app.route("/spaces/<space_id>", methods=["GET"])
def get_space(space_id):
    """GET /spaces/<space_id> - Obtiene un espacio por ID."""
    try:
        space = space_service.get_space(space_id)
        return jsonify(format_space(space)), 200
    except SpaceNotFoundError:
        logger.warning(f"Espacio no encontrado: {space_id}")
        return error_response(f"Espacio '{space_id}' no encontrado", 404)
    except Exception as e:
        logger.error(f"Error al obtener espacio {space_id}: {str(e)}")
        return error_response(f"Error al obtener espacio: {str(e)}", 500)

# ============================================================================
# RESERVAS - LECTURA
# ============================================================================

@app.route("/bookings", methods=["GET"])
def list_bookings():
    """GET /bookings - Lista todas las reservas."""
    try:
        bookings = booking_service.list_bookings()
        return jsonify([format_booking(b) for b in bookings]), 200
    except Exception as e:
        logger.error(f"Error al listar reservas: {str(e)}")
        return error_response(f"Error al listar reservas: {str(e)}", 500)


@app.route("/bookings/<booking_id>", methods=["GET"])
def get_booking(booking_id):
    """GET /bookings/<booking_id> - Obtiene una reserva por ID."""
    try:
        booking = booking_service.get_booking(booking_id)
        return jsonify(format_booking(booking)), 200
    except BookingNotFoundError:
        logger.warning(f"Reserva no encontrada: {booking_id}")
        return error_response(f"Reserva '{booking_id}' no encontrada", 404)
    except Exception as e:
        logger.error(f"Error al obtener reserva {booking_id}: {str(e)}")
        return error_response(f"Error al obtener reserva: {str(e)}", 500)


@app.route("/spaces/disponibles/<fecha_inicio>/<fecha_fin>", methods=["GET"])
def get_available_spaces(fecha_inicio, fecha_fin):
    """GET /spaces/disponibles/<fecha_inicio>/<fecha_fin> - Espacios libres en rango.

    Formato: ISO 8601, ej: 2026-04-25T09:00:00
    """
    try:
        start = datetime.fromisoformat(fecha_inicio)
        end = datetime.fromisoformat(fecha_fin)
        spaces = space_service.get_available_spaces(start, end)
        return jsonify([format_space(s) for s in spaces]), 200
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
    """POST /bookings/nueva/<user_name>/<space_name>/<fecha_inicio>/<fecha_fin>
    - Crea una reserva."""
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
# BÚSQUEDAS POR USUARIO Y ESPACIO (GET)
# ============================================================================

@app.route("/bookings/usuario/<user_name>", methods=["GET"])
def get_bookings_for_user_route(user_name):
    """GET /bookings/usuario/<user_name> - Reservas de un usuario."""
    try:
        bookings = booking_service.get_bookings_for_user(user_name)
        return jsonify([format_booking(b) for b in bookings]), 200
    except ValueError as e:
        logger.warning(f"Usuario no encontrado: {user_name}")
        return error_response(str(e), 404)
    except Exception as e:
        logger.error(f"Error al obtener reservas: {str(e)}")
        return error_response(f"Error al obtener reservas: {str(e)}", 500)


@app.route("/bookings/espacio/<space_name>", methods=["GET"])
def get_bookings_for_space_route(space_name):
    """GET /bookings/espacio/<space_name> - Reservas de un espacio."""
    try:
        bookings = booking_service.get_bookings_for_space(space_name)
        return jsonify([format_booking(b) for b in bookings]), 200
    except ValueError as e:
        logger.warning(f"Espacio no encontrado: {space_name}")
        return error_response(str(e), 404)
    except Exception as e:
        logger.error(f"Error al obtener reservas: {str(e)}")
        return error_response(f"Error al obtener reservas: {str(e)}", 500)

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 Iniciando SmartSpaces API con observabilidad global...")
    print("📌 Base de datos: smartspaces.db")
    print("📊 Logging: smartspaces.log")
    print("🌐 Servidor: http://localhost:5000")
    print("📚 Ayuda: http://localhost:5000/ayuda")
    print("=" * 80)
    logger.info("Iniciando servidor Flask")
    app.run(debug=True, host="0.0.0.0", port=5000)