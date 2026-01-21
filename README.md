## **Descripción general** 
El proyecto consiste en el diseño y desarrollo de un **Sistema de Gestión de Espacios Inteligentes**, orientado a la administración y optimización del uso de espacios físicos compartidos dentro de una organización, como pueden ser aulas, salas de reuniones, puestos de trabajo o salas polivalentes.

El sistema modela un conjunto de espacios reservables y un conjunto de usuarios con distintos roles, permitiendo gestionar **reservas temporales** de dichos espacios bajo una serie de normas y restricciones definidas por el propio sistema. Estas normas se aplican automáticamente en función tanto del tipo de usuario como de las características del espacio reservado. 

Aunque el proyecto se inspira en aplicaciones reales utilizadas en empresas, universidades o espacios de coworking, su objetivo principal es **simular el funcionamiento lógico del sistema**, centrándose en el diseño orientado a objetos, la coherencia de las operaciones y la correcta relación entre los distintos elementos del modelo.

## **Objetivos**
### **Objetivo general**
Desarrollar un sistema modular basado en Programación Orientada a Objetos que permita gestionar espacios compartidos y sus reservas de forma coherente, evitando conflictos y garantizando el cumplimiento de las reglas de uso establecidas.

### **Objetivos específicos** 
- Modelar usuarios con distintos roles y capacidades dentro del sistema. 
- Representar espacios físicos con características y restricciones diferenciadas. 
- Gestionar reservas asegurando la disponibilidad de los espacios y evitando solapamientos. 
- Aplicar reglas automáticas en función del tipo de usuario y del tipo de espacio. 
- Utilizar herencia y herencia múltiple para favorecer la reutilización de código y la escalabilidad del sistema.

## **Características principales** 
### **Gestión de usuarios** 
- El sistema contemplará **usuarios genéricos** con información común, como identificador y nombre. 
- Se definirán **distintos tipos de usuarios**, por ejemplo: 
  - Usuarios básicos, con límites estrictos de uso. 
  - Usuarios premium, con mayor flexibilidad en reservas. 
  - Administradores, con permisos de gestión global del sistema. 
- Cada tipo de usuario tendrá reglas propias, como: 
  - Número máximo de reservas activas. 
  - Duración máxima permitida de una reserva. 
- Mediante herencia múltiple, un usuario podrá incorporar **comportamientos adicionales**, como prioridad en las reservas o límites ampliados, sin necesidad de duplicar código.

### **Gestión de espacios** 
- Los espacios representarán los **recursos físicos disponibles para su reserva** dentro de la organización. 
- Se gestionarán **distintos tipos de espacios**, tales como: 
  - Aulas. 
  - Salas de reuniones. 
  - Puestos de trabajo. 
  - Salas polivalentes. 
- Cada espacio contará con información común como identificador, nombre, capacidad y estado (disponible, reservado o en mantenimiento). 
- Mediante herencia, cada tipo de espacio podrá definir reglas específicas de uso.

### **Características avanzadas y herencia múltiple en espacios** 
Además del tipo básico de espacio, algunos espacios podrán incorporar **características adicionales**, implementadas mediante herencia múltiple: 

- Espacios con equipamiento especial (proyector, sistemas de videoconferencia, sonido). 
- Espacios con restricciones horarias. 
- Espacios premium con condiciones de acceso específicas. 

De este modo, un mismo espacio podrá pertenecer a una categoría funcional y, al mismo tiempo, disponer de características adicionales, evitando la creación de clases rígidas y poco escalables.

### **Reservas y control de disponibilidad** 
- Las **reservas** relacionan un usuario con un espacio durante un intervalo de tiempo determinado. 
- El sistema comprobará automáticamente: 
  - La disponibilidad del espacio. 
  - La inexistencia de solapamientos con otras reservas. 
  - Que el usuario cumpla los permisos necesarios. 
  - Que se respeten las reglas propias del espacio. 
- Las reservas podrán encontrarse en distintos estados, como activas, canceladas o finalizadas.

## **Diseño orientado a objetos** 
El proyecto hará uso de los principales principios de la Programación Orientada a Objetos: 

- **Encapsulación**, para proteger los datos y controlar las operaciones válidas. 
- **Herencia**, para modelar distintos tipos de usuarios y espacios a partir de clases base. 
- **Herencia múltiple**, para añadir comportamientos adicionales como prioridades, equipamiento o restricciones horarias. 
- **Polimorfismo**, permitiendo tratar de forma uniforme a distintos tipos de usuarios y espacios.

## **Acciones y consultas disponibles** 
El sistema permitirá realizar, entre otras, las siguientes acciones: 

- Registrar, modificar y eliminar usuarios. 
- Registrar, modificar y desactivar espacios. 
- Consultar la disponibilidad de los espacios. 
- Crear, cancelar y finalizar reservas. 
- Listar reservas activas por usuario o por espacio. 
- Detectar y evitar operaciones no válidas, como reservas solapadas o accesos no autorizados.

## **Alcance del proyecto** 
### **Incluye** 
- Modelado de usuarios, espacios y reservas. 
- Gestión de distintos tipos de usuarios y espacios con comportamientos diferenciados. 
- Implementación de herencia y herencia múltiple de forma justificada. 
- Control de estados y validación de reglas de uso. 
- Verificaciones que impidan estados u operaciones incoherentes. 

### **No incluye** 
- Interfaces gráficas o aplicaciones web. 
- Persistencia en bases de datos. 
- Integración con sistemas externos de pago, sensores o notificaciones. 
