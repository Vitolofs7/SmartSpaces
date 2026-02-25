REVISIONES

## REVISIÓN FASE 03 - 2026-02-25

### Incumplimientos detectados

1. Falta procedimiento explícito de cobertura con comandos ejecutables (`run/report/html`).
Evidencia:
- `docs/TESTS_AND_STEPS.md:129` -> solo indica "check test coverage".
- `docs/TESTS_AND_STEPS.md:135-140` -> lista porcentajes, sin comandos `coverage run`, `coverage report`, `coverage html`.

Recomendación:
- Añadir en `docs/TESTS_AND_STEPS.md` el flujo completo con comandos de cobertura y el orden de ejecución.

## REVISIÓN FASE 02 - 2026-02-25

### RESULTADO DE LA REVISIÓN DE DOCUMENTACIÓN

### Incumplimientos detectados

1. La documentación de dependencias se contradice.
Evidencia:
- `README.md:112` -> `No external dependencies (all data in-memory for simulation).`
- `docs/EXECUTION.md:9` -> `No external libraries or frameworks are required`
- `requirements.txt:1` -> `coverage`

Explicación:
- En docs se afirma que no hay dependencias externas.
- En el repositorio sí hay al menos una dependencia declarada para pruebas (`coverage`).

2. Falta documentación base dentro de `docs/`.
Evidencia:
- `docs/README.md` -> archivo vacío (0 bytes).

3. Se documentan roles de usuario que el modelo de dominio actual no implementa.
Evidencia:
- `README.md:68` -> `Basic Users`
- `README.md:69` -> `Premium Users`
- `README.md:70` -> `Administrators`
- `domain/user.py:6` -> `class User:`

4. Inconsistencia de nomenclatura en estados.
Evidencia:
- `docs/BUSINESS_RULES.md:100` -> `CANCELED`
- `docs/BUSINESS_RULES.md:108` -> `A CANCELED or FINISHED...`
- `domain/booking.py:17` -> `STATUS_CANCELLED = "CANCELLED"`

5. El menú documentado no coincide con el menú real de la aplicación.
Evidencia:
- `docs/EXECUTION.md:47` -> `8. Exit`
- `docs/USE_CASES.md:238-247` -> `UC-8: Exit Application` en opción `8`
- `presentation/menu.py:25` -> `9. Modify booking`
- `presentation/menu.py:26` -> `10. Exit`

Explicación:
- La documentación sigue describiendo salida en opción 8, pero el código actual expone 10 opciones y la salida real está en la opción 10.

6. La versión mínima de Python es inconsistente entre documentos.
Evidencia:
- `docs/TESTS_AND_STEPS.md:13` -> `Python >= 3.13`
- `README.md:111` -> `Python 3.9+`
- `docs/EXECUTION.md:7` -> `Python 3.9 or higher`

### Incumplimientos de nombres

7. Nombre de clase no consistente con PascalCase recomendado.
Evidencia:
- `domain/space_meetingroom.py:6` -> `class SpaceMeetingroom(Space):`

Recomendación:
- Renombrar a `SpaceMeetingRoom` para mantener un PascalCase claro y consistente.

8. Uso de abreviaturas de una letra en variables que ocultan intención.
Evidencia:
- `application/booking_service.py:92` -> `b = self._booking_repo.get(booking_id)`
- `application/booking_service.py:146` -> `u = self._find_user_by_name(user_name)`
- `application/booking_service.py:158` -> `s = self._find_space_by_name(space_name)`
- `presentation/menu.py:145` -> `for b in booking_service.list_bookings()`
- `presentation/menu.py:141` -> `for u in user_service.list_users()`
- `presentation/menu.py:137` -> `for s in space_service.list_spaces()`

- El criterio indica evitar abreviaturas poco descriptivas (`tmp`, `aux`, etc.). Variables como `b`, `u`, `s` dificultan leer qué representa cada dato en flujos largos.

Recomendación:
- Usar nombres explícitos (`booking`, `user`, `space`) en lugar de abreviaturas de una letra.

9. Nombres de colecciones genéricos y poco orientados al dominio.
Evidencia:
- `infrastructure/booking_memory_repository.py:15` -> `self._data, self._last_id = {}, 0`
- `infrastructure/space_memory_repository.py:15` -> `self._data = {}`
- `infrastructure/user_memory_repository.py:15` -> `self._data = {}`

- El criterio recomienda describir intención y usar vocabulario del dominio. `_data` es demasiado genérico y no comunica si almacena bookings, spaces o users.

Recomendación:
- Renombrar colecciones a nombres de dominio en plural (`bookings_by_id`, `spaces_by_id`, `users_by_id`).

10. Nombres con unidades no explícitas en reglas de duración.
Evidencia:
- `domain/user.py:38` -> `self._max_booking_duration = timedelta(hours=2)`
- `domain/user.py:94` -> `def max_booking_duration(self):`

- El criterio indica incluir unidades cuando aplique. Aquí se maneja una duración en horas, pero el nombre no explicita unidad y obliga a mirar implementación.

Recomendación:
- Usar nombres que indiquen unidad o forma (`max_booking_duration_hours` o documentar explícitamente la unidad en el nombre de la regla).

### Incumplimientos de documentación inline

11. Falta docstring de módulo en archivos principales (la primera línea no es `"""..."""`).
Evidencia:
- `presentation/menu.py:1` -> `# presentation/menu.py`
- `application/booking_service.py:1` -> `# application/booking_service.py`
- `application/space_service.py:1` -> `# application/space_service.py`
- `application/user_service.py:1` -> `# application/user_service.py`
- `domain/booking.py:1` -> `# domain/booking.py`
- `domain/space.py:1` -> `# domain/space.py`
- `domain/user.py:1` -> `# domain/user.py`
- `infrastructure/seed_data.py:1` -> `# infrastructure/seed_data.py`

12. Clases de tests sin docstring de clase.
Evidencia:
- `tests/domain/test_booking.py:6` -> `class FakeUser:`
- `tests/domain/test_booking.py:14` -> `class FakeSpace:`
- `tests/domain/test_booking.py:34` -> `class FakeBookingRepo:`
- `tests/domain/test_booking.py:45` -> `class TestBooking(unittest.TestCase):`
- `tests/domain/test_space.py:4` -> `class TestSpace(unittest.TestCase):`
- `tests/domain/test_user.py:5` -> `class TestUser(unittest.TestCase):`
- `tests/domain/test_integration.py:8` -> `class TestIntegrationBookingSystem(unittest.TestCase):`

Recomendación:
- Añadir una línea de docstring por clase de test explicando su objetivo y alcance de validación.

13. Comentarios de línea que repiten lo obvio en lugar de explicar "por qué".
Evidencia:
- `presentation/menu.py:136` -> `# List all spaces`
- `presentation/menu.py:139` -> `# List all users`
- `presentation/menu.py:143` -> `# List all bookings`
- `presentation/menu.py:148` -> `# Create a new booking`
- `presentation/menu.py:155` -> `# Cancel a booking`
- `presentation/menu.py:159` -> `# Finish a booking`
- `presentation/menu.py:163` -> `# Create a new space or meeting room`
- `presentation/menu.py:166` -> `# List available spaces for a given date range`
- `presentation/menu.py:176` -> `# Modify an existing booking`
- `presentation/menu.py:182` -> `# Exit the program`

- El criterio pide evitar ruido y no comentar lo evidente.

### Incumplimientos de estructura documental del proyecto

14. Falta índice utilizable en `docs/README.md` (archivo de entrada de la carpeta `docs`).
Evidencia:
- `docs/README.md` existe pero está vacío (0 bytes).

## REVISIÓN FASE 01 - 2026-02-25

### Incumplimientos detectados

1. El contrato de repositorio documentado no coincide con la implementación real.
Evidencia:
- `docs/REPOSITORY_CONTRACT.md:65` -> `Raises an error if the entity does not exist.`
- `infrastructure/space_memory_repository.py:34` -> `return self._data.get(space_id)`
- `infrastructure/user_memory_repository.py:34` -> `return self._data.get(user_id)`
- `infrastructure/booking_memory_repository.py:39` -> `return self._data.get(booking_id)`

Explicación:
- La documentación dice que `get` lanza error cuando no existe entidad.
- Las implementaciones reales usan `.get(...)`, que devuelve `None` y no lanza excepción.

Cómo arreglarlo:
- Definir un comportamiento único para `get` y sincronizar documentación e implementación.

2. Bug en cancelación/finalización por doble liberación del espacio.
Evidencia:
- `application/booking_service.py:95` -> `b.cancel()`
- `application/booking_service.py:96` -> `b.space.release()`
- `application/booking_service.py:113` -> `b.finish()`
- `application/booking_service.py:114` -> `b.space.release()`
- `domain/booking.py:132-140` -> `cancel()` ya libera el espacio.
- `domain/booking.py:142-150` -> `finish()` ya libera el espacio.

En servicio se libera el espacio dos veces: una dentro de `cancel()/finish()` y otra inmediatamente después con `b.space.release()`.

Eso puede provocar error de estado (`Space not reserved`) en ejecución real.

3. Disponibilidad temporal incoherente con la lógica de solape.

Ahora mismo el código decide si un espacio se puede reservar usando **dos reglas distintas a la vez**:

1. Regla por estado global del espacio  
- En `domain/booking.py:61` se pide que `space.is_available()` sea `True`.  
- Pero cuando se crea una reserva, `domain/space.py:161-168` cambia el espacio a `RESERVED` para todo el sistema.

2. Regla por solape de fechas  
- En `domain/booking.py:64` también se comprueba si la nueva reserva se cruza en tiempo con otra.

El problema:
- Si existe una reserva activa hoy (por ejemplo de 10:00 a 11:00), el espacio queda en estado global `RESERVED`.
- Luego intentas reservar ese mismo espacio para mañana (sin solape), pero puede fallar antes por estado global, aunque por fechas sería válido.
- Es decir: la regla temporal (solape) dice "sí se puede", pero la regla global de estado dice "no", y se contradicen.

Por eso se considera incoherente:
- Estás modelando disponibilidad "por agenda/horario" y "por estado único global" al mismo tiempo.
- Para reservas con fecha/hora, normalmente debe mandar la agenda temporal (solapes), no un bloqueo global permanente hasta cancelar/finalizar.

Sugerencia:
- Quita en creación de reserva la dependencia de `space.is_available()` para casos con fecha/hora.
- Decide disponibilidad solo con "no solapa con reservas activas del mismo espacio".
- Mantén `MAINTENANCE` como bloqueo global (eso sí tiene sentido global).
- Deja `RESERVED` como estado derivado para mostrar en UI, no como criterio de rechazo de nuevas reservas futuras.
- Centraliza esa regla en un único sitio (dominio o servicio, pero solo uno).


4. Reglas de usuario definidas pero no aplicadas en casos de uso de reserva.
Evidencia:
- `domain/user.py:37` -> `_max_active_bookings = 1`
- `domain/user.py:38` -> `_max_booking_duration = timedelta(hours=2)`
- `domain/user.py:89-96` -> propiedades públicas de esos límites.
- `application/booking_service.py:31-59` -> `create_booking` no valida esos límites.
- `application/booking_service.py:61-80` -> `modify_booking` no valida duración máxima de usuario.

Explicación:
- El dominio expone políticas de reserva por usuario, pero el servicio no las usa para aceptar/rechazar reservas.
- La regla existe en código, pero no se hace cumplir en el flujo principal.

5. Duplicación de validación/persistencia en creación de reservas.
Evidencia:
- `application/booking_service.py:54` -> `_check_overlap(...)` en servicio.
- `domain/booking.py:64` -> validación de solape también en dominio.
- `domain/booking.py:67` -> `Booking.create(...)` guarda en repositorio.
- `application/booking_service.py:57` -> servicio vuelve a guardar el booking.

Explicación:
- El mismo control (solape) y parte de la persistencia se ejecutan en dos capas diferentes.
- Esto añade complejidad y riesgo de inconsistencias.

6. Acoplamiento de presentación con persistencia en consulta de disponibilidad.
Evidencia:
- `presentation/menu.py:168` -> pasa `booking_repo` al servicio.
- `application/space_service.py:80` -> `get_available_spaces(self, booking_repo, start, end)`.
- `application/space_service.py:94` -> consulta directa `booking_repo.list()` dentro del servicio.

Este caso de uso (buscar espacios disponibles) debería ser responsabilidad completa de la capa de aplicación. Pero ahora la capa de presentación está participando en cómo se accede a datos.

## REVISIÓN FASE 01 - 2026-02-03

## RECOMENDACIONES / COMENTARIOS

- Analiza como está construida la aplicación de la máquina expendedora y trata de aplicar los mismos principios a tu supuesto.
- Empieza por una entidad, por ejemplo las reservas, y vete implementando todas las capas de las reservas.

## ASPECTOS A CAMBIAR / AÑADIR

- En el menú (presentación)
  - [x] En las opciones 1 y 2 del menú accedes directamente al repositorio para mostrar datos. Deberías pasar la petición a un servicio de la aplicación que debería llamar al dominio para que se encargue de obtener dichos datos.
  - [ ] En la opción 4 el booking_id no se debe crear ni aquí, ni en el servicio, sino en el dominio. Tampoco es lógico que el usuario tenga que poner user_id o space_id sino nombres.
    - Comentario: está corregido que no se pidan IDs al usuario (se usan nombres en `presentation/menu.py:149-152`) y tampoco se genera en menú/servicio (`application/booking_service.py:55-57`), pero el `booking_id` se asigna en infraestructura (`infrastructure/booking_memory_repository.py:25-28`) y en dominio nace como `None` (`domain/booking.py:33`), por eso este punto sigue sin cerrarse según el criterio original.
  - [x] En la opción 7 creas directamente en esta capa un objeto del dominio y lo almacenas saltándote el diseño por capas. Deberías pasar los datos leidos al servicio y este encargarse de pasarlos al dominio para que aplique la lógica de negocio que incluye almacenarlos.

- En el dominio
    - [ ] El añadir una entidad el id no deberías introducirlo a mano, sino cada vez que añades al repo miras el id del último objeto almacenado y le sumas 1. O en el repo tienes un atributo que sea el último id usado (o disponible)
    - Comentario: corregido solo para reservas (`infrastructure/booking_memory_repository.py:15,25-28`). En espacios el ID todavía se introduce manualmente desde menú (`presentation/menu.py:100`) y se pasa al servicio (`application/space_service.py:27,42-44`).
