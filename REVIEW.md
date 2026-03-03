# Revisión del proyecto — Víctor

**Fuente de verdad:** `SmartSpaces/` (código en raíz del repositorio, sin carpetas numeradas de fase)
**Fases detectadas:** Sin carpetas numeradas; el contenido equivale a la fase 03 (Testing)


## REVISIÓN FASE 03 - 2026-03-03 — Nota: 8,5/10

### Resuelto desde la revisión anterior

- Añadida la carpeta `tests/` con estructura de paquetes (`tests/__init__.py`, `tests/domain/__init__.py`) y tests para `Booking`, `Space`, `User` e integración: 28 tests, todos pasan.
- `requirements.txt` creado con `coverage` como dependencia.
- `docs/TESTS_AND_STEPS.md` expandido con la descripción de cada fichero de test y lo que valida cada caso.

### Cumple

- Tests organizados en `tests/domain/` con `__init__.py` en cada nivel de paquete.
- Tests unitarios para las tres clases del dominio (`Booking`, `Space`, `User`) y test de integración del flujo completo.
- Los 28 tests pasan: `Ran 28 tests in 0.000s — OK`.
- `coverage` declarado en `requirements.txt`.
- `docs/TESTS_AND_STEPS.md` documenta qué valida cada fichero de test.
- `CHANGELOG.md` actualizado con versión `0.3.0` hasta `0.3.4`, con secciones Added/Changed/Fixed.
- `README.md` actualizado con la estructura del proyecto y las instrucciones de ejecución.

### Errores y aspectos a mejorar

- **[IMPORTANTE] `docs/TESTS_AND_STEPS.md` — No incluye los comandos para ejecutar la cobertura.** La sección 4 muestra porcentajes de cobertura pero no cómo reproducirlos. El criterio de la fase exige documentar la ejecución de `coverage`.
  - *Cómo resolverlo:* Añade una subsección con la secuencia completa: `pip install -r requirements.txt`, después `coverage run -m unittest`, luego `coverage report` y opcionalmente `coverage html`.

- **[IMPORTANTE] `docs/EXECUTION.md` — No está actualizado para la fase 03.** El documento no menciona cómo ejecutar los tests ni cómo obtener el informe de cobertura. 
  - *Cómo resolverlo:* Añade una sección "Running tests" con los comandos de tests y cobertura. 


## REVISIÓN FASE 02 - 2026-03-03 — Nota: 7,5/10

### Cumple

- `CHANGELOG.md` muy bien estructurado con secciones Added/Changed/Fixed/Security desde `0.1.0` hasta `0.3.4`.
- `README.md` completo: descripción, objetivos, entidades principales, arquitectura, estructura del proyecto e instrucciones de instalación y ejecución.
- Docstrings completos en clases y métodos públicos del dominio, servicios e infraestructura, con `Args`, `Returns` y `Raises`.
- Reglas de negocio documentadas en `docs/BUSINESS_RULES.md`: creación, estados, transiciones y cancelación para espacios, salas de reuniones, usuarios y reservas.
- `docs/` contiene: `DESCRIPTION_AND_SCOPE.md`, `LAYERED_ARCHITECTURE.md`, `USE_CASES.md`, `BUSINESS_RULES.md`, `DOMAIN_MODEL.md`, `REPOSITORY_CONTRACT.md`, `INITIAL_DATA.md`, `EXECUTION.md`, `TESTS_AND_STEPS.md`.

### Errores y aspectos a mejorar

- **[IMPORTANTE] `docs/README.md` — El fichero existe pero está vacío.** La carpeta `docs/` debería tener un fichero de entrada que explique qué contiene cada documento.
  - *Cómo resolverlo:* Escribe un índice con una línea descriptiva por cada fichero de `docs/` y una referencia o enlace a él.

- **[IMPORTANTE] Falta `docs/TROUBLESHOOTING.md`.** 

- **[IMPORTANTE] `README.md:64-77` — Se documentan tres tipos de usuario (`Basic Users`, `Premium Users`, `Administrators`) que no están implementados en el código.** Solo existe la clase `User` genérica en `domain/user.py`.
  - *Cómo resolverlo:* O bien implementa los roles como subclases de `User` con distintos límites, o bien elimina esa sección del `README.md` y describe solo lo que realmente existe.

- **[IMPORTANTE] Falta docstring en módulos**

- **[SUGERENCIA] Nombres que no siguen convenciones o no se utilizan.** Revisa y corrige los siguientes casos:
  - `domain/space_meetingroom.py:6` — Clase `SpaceMeetingroom`: "Room" es palabra independiente, debe ser `SpaceMeetingRoom`.
  - `domain/space_meetingroom.py:61,83,105,114` — Parámetro `v` en los setters: usa el nombre del atributo que recibe (`room_number`, `floor`, `num_power_outlets`).
  - `domain/space_meetingroom.py:202` — Parámetro `n` en `can_accommodate`: renombra a `num_people` o `people_count`.
  - `domain/space_meetingroom.py:48` — Variable local `eq` en `__str__`: renombra a `equipment_display`.
  - `infrastructure/*_memory_repository.py:15` — Atributo `_data` en los tres repositorios: no indica qué almacena; usa `_bookings`, `_spaces`, `_users`.
  - `application/booking_service.py:92,146,158`, `presentation/menu.py:137,141,145` — Variables de una letra `b`, `u`, `s`: usa `booking`, `user`, `space`.
  - `domain/booking.py:18` — `_id_counter = 1` es atributo de clase que nunca se usa; elimínalo.
  - `domain/space.py:45` — `self._bookings = {}` se define pero nunca se usa; elimínalo.
  - Servicios — `BookingService` usa `_booking_repo` y `SpaceService` usa `_space_repo`, pero `UserService` usa `_user_repository`. Elige una convención y aplícala en los tres.
 
 - **[SUGERENCIA] Comentarios que repiten lo obvio**. `presentation/menu.py:136,139,143,148,155,159,163,166,176` —  (`# List all spaces`, etc.): elimínalos.

 - **[TYPO]** `docs/BUSINESS_RULES.md:100,108` — Usa `CANCELLED` en lugar de `CANCELED` para coincidir con el código.

## REVISIÓN FASE 01 - 2026-03-03 — Nota: 8,5/10

### Cumple

- Proyecto organizado en las cuatro capas: `domain/`, `application/`, `infrastructure/`, `presentation/`, cada una con su `__init__.py`.
- POO bien aplicado: atributos privados con doble guion bajo y propiedades, herencia (`SpaceMeetingroom` extiende `Space` con `super().__init__`), validaciones propias en cada entidad.
- Contrato de repositorio definido en el dominio (`BookingRepository`, `SpaceRepository`, `UserRepository`) e implementaciones en infraestructura.
- El menú delega en los servicios de aplicación y no accede directamente al dominio ni a los repositorios (salvo el problema señalado abajo).
- `README.md` con instrucciones de instalación y ejecución.

### Errores y aspectos a mejorar

- **[BUG] `application/booking_service.py:95-96` y `113-114` — Las opciones 5 (Cancelar) y 6 (Finalizar) del menú siempre fallan con `ValueError: Space not reserved`.** `b.cancel()` ya llama internamente a `space.release()` (`domain/booking.py:139`), que cambia el estado del espacio de `RESERVED` a `AVAILABLE`. El servicio vuelve a llamar a `b.space.release()` sobre un espacio ya disponible, lo que lanza la excepción en `domain/space.py:176`. El mismo error ocurre en `finish_booking`.
  - *Cómo resolverlo:* Elimina del servicio las líneas `b.space.release()` y `self._space_repo.save(b.space)` que aparecen después de `b.cancel()` / `b.finish()`. El dominio ya gestiona el estado del espacio; el servicio solo necesita llamar al método del dominio y guardar la reserva.

- **[DISEÑO] `application/space_service.py:80` — `get_available_spaces` recibe `booking_repo` directamente desde la capa de presentación (`presentation/menu.py:168`).** La presentación no debe conocer ni manejar repositorios.
  - *Cómo resolverlo:* Inyecta el repositorio de reservas en el constructor de `SpaceService` como se hace en `BookingService`, y elimina el parámetro `booking_repo` del método.

- **[DISEÑO] `domain/user.py:37-38` — Las reglas de usuario (`max_active_bookings`, `max_booking_duration`) están definidas en el dominio pero no se aplican en ningún caso de uso.** `BookingService.create_booking` no valida si el usuario supera sus límites.
  - *Cómo resolverlo:* En `create_booking`, comprueba cuántas reservas activas tiene el usuario y valida que `end_time - start_time` no supere `user.max_booking_duration`.

- **[DISEÑO] `domain/booking.py:61` y `64` — Conviven dos mecanismos de disponibilidad que se contradicen.** La creación exige `space.is_available()` (estado global AVAILABLE) y además comprueba solapes por fecha. Pero al crear una reserva el espacio queda en `RESERVED` globalmente, impidiendo reservar ese mismo espacio para una fecha futura aunque no haya solape.
  - *Cómo resolverlo:* Basa la disponibilidad únicamente en la ausencia de solapes temporales. Mantén `MAINTENANCE` como bloqueo global, pero no uses el estado `RESERVED` como condición de rechazo para nuevas reservas.


## REVISIÓN FASE 03 - 2026-02-25

### Incumplimientos detectados

1. Falta procedimiento explícito de cobertura con comandos ejecutables (`run/report/html`).
Evidencia:
- `docs/TESTS_AND_STEPS.md:129` -> solo indica "check test coverage".
- `docs/TESTS_AND_STEPS.md:135-140` -> lista porcentajes, sin comandos `coverage run`, `coverage report`, `coverage html`.

Recomendación:
- Añadir en `docs/TESTS_AND_STEPS.md` el flujo completo con comandos de cobertura y el orden de ejecución.

---

## REVISIÓN FASE 02 - 2026-02-25

### Incumplimientos detectados

1. La documentación de dependencias se contradice.
Evidencia:
- `README.md:112` -> `No external dependencies (all data in-memory for simulation).`
- `docs/EXECUTION.md:9` -> `No external libraries or frameworks are required`
- `requirements.txt:1` -> `coverage`

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
- `domain/booking.py:17` -> `STATUS_CANCELLED = "CANCELLED"`

5. El menú documentado no coincide con el menú real de la aplicación.
Evidencia:
- `docs/EXECUTION.md:47` -> `8. Exit`
- `presentation/menu.py:25` -> `9. Modify booking`
- `presentation/menu.py:26` -> `10. Exit`

6. La versión mínima de Python es inconsistente entre documentos.
Evidencia:
- `docs/TESTS_AND_STEPS.md:13` -> `Python >= 3.13`
- `README.md:111` -> `Python 3.9+`
- `docs/EXECUTION.md:7` -> `Python 3.9 or higher`

### Incumplimientos de nombres

7. `domain/space_meetingroom.py:6` -> `class SpaceMeetingroom(Space):` — Renombrar a `SpaceMeetingRoom`.

8. Variables de una letra (`b`, `u`, `s`) en servicio y menú.

9. Colecciones genéricas `self._data` en repositorios — renombrar a `bookings_by_id`, `spaces_by_id`, `users_by_id`.

10. `domain/user.py:94` -> `max_booking_duration` sin indicar unidad.

### Incumplimientos de documentación inline

11. Módulos sin docstring (usan comentario `# ruta/fichero.py` en vez de `"""..."""`).

12. Clases de test sin docstring de clase.

13. Comentarios evidentes en el menú (`# List all spaces`, `# List all users`, etc.).

14. `docs/README.md` existe pero está vacío.

---

## REVISIÓN FASE 01 - 2026-02-25

### Incumplimientos detectados

1. El contrato de repositorio documentado no coincide con la implementación.
Evidencia:
- `docs/REPOSITORY_CONTRACT.md:65` -> `Raises an error if the entity does not exist.`
- `infrastructure/space_memory_repository.py:34` -> `return self._data.get(space_id)` (devuelve `None`, no lanza excepción)

2. Bug en cancelación/finalización por doble liberación del espacio.
Evidencia:
- `application/booking_service.py:95-96` -> `b.cancel()` + `b.space.release()`
- `domain/booking.py:132-140` -> `cancel()` ya libera el espacio internamente.

3. Disponibilidad temporal incoherente: estado global `RESERVED` bloquea reservas futuras sin solape.

4. Reglas de usuario (`max_active_bookings`, `max_booking_duration`) definidas en dominio pero no aplicadas en el servicio.

5. Duplicación de validación de solape: en dominio (`domain/booking.py:64`) y en servicio (`application/booking_service.py:54`).

6. Acoplamiento de presentación con persistencia: `presentation/menu.py:168` pasa `booking_repo` directamente al servicio.

---

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
