# REVISIÓN FASE 01

## RECOMENDACIONES / COMENTARIOS

- Analiza como está construida la aplicación de la máquina expendedora y trata de aplicar los mismos principios a tu supuesto.
- Empieza por una entidad, por ejemplo las reservas, y vete implementando todas las capas de las reservas.

## ASPECTOS A CAMBIAR / AÑADIR

- En el menú (presentación)
  - En las opciones 1 y 2 del menú accedes directamente al repositorio para mostrar datos. Deberías pasar la petición a un servicio de la aplicación que debería llamar al dominio para que se encargue de obtener dichos datos.
  - En la opción 4 el booking_id no se debe crear ni aquí, ni en el servicio, sino en el dominio. Tampoco es lógico que el usuario tenga que poner user_id o space_id sino nombres.
  - En la opción 7 creas directamente en esta capa un objeto del dominio y lo almacenas saltándote el diseño por capas. Deberías pasar los datos leidos al servicio y este encargarse de pasarlos al dominio para que aplique la lógica de negocio que incluye almacenarlos.

- En el servicio (aplicación)
  - Haces operaciones que corresponden al dominio: aplicas las reglas de la lógica de negocio y almacenas las reservas, espacios y usuarios.

- En el dominio
  - Debería haber clases para las reservas, espacios y usuarios que tengan un atributo que sea un repositorio y se encarguen de gestionar el acceso a los mismos. Debería estar organizado como de la misma forma que en la máquina expendedora se guardan todos los productos de la máquina.
  - El añadir una entidad el id no deberías introducirlo a mano, sino cada vez que añades al repo miras el id del último objeto almacenado y le sumas 1. O en el repo tienes un atributo que sea el último id usado (o disponible)