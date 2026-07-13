# Prompt para reconstrucción del proyecto Flask D1

```text
Actúa como un Arquitecto de Software Senior con más de 15 años de experiencia en desarrollo de aplicaciones empresariales utilizando:

• Python 3
• Flask
• PostgreSQL
• psycopg2
• Jinja2
• HTML5
• CSS3
• Bootstrap 5
• JavaScript
• Arquitectura MVC
• Optimización SQL
• Diseño de aplicaciones CRUD empresariales

IMPORTANTE

Voy a suministrarte únicamente los siguientes archivos:

- app.py
- conexion.py
- config.py
- Tablas.sql

NO debes asumir absolutamente nada que no esté en dichos archivos.

El archivo Tablas.sql será la ÚNICA fuente de verdad respecto a la estructura de la base de datos.

Debes respetar exactamente:

• nombres de tablas
• nombres de columnas
• tipos de datos
• restricciones
• claves primarias
• claves foráneas
• índices existentes
• relaciones

NO puedes renombrar tablas.

NO puedes renombrar columnas.

NO puedes modificar el modelo relacional.

NO puedes inventar columnas.

Si encuentras inconsistencias entre el código Python y la base de datos, SIEMPRE debes adaptar el código Python a Tablas.sql.

==========================================================

OBJETIVO

Reconstruir completamente el Website de una empresa tipo D1 desarrollado en Flask.

No quiero pequeñas correcciones.

Quiero un proyecto completamente profesional.

Quiero que reconstruyas todos los archivos necesarios para que el proyecto quede completamente funcional.

Puedes modificar completamente:

app.py

conexion.py

config.py

Puedes crear cualquier archivo adicional que sea necesario.

==========================================================

EL PROYECTO DEBE ESTAR DESARROLLADO EN

Python + Flask

No Django.

No FastAPI.

No SQLAlchemy.

Toda la conexión debe realizarse utilizando:

psycopg2

mediante

conexion.py

No deben existir conexiones repetidas en otros archivos.

Toda operación sobre PostgreSQL debe utilizar la función de conexión definida en conexion.py.

==========================================================

ARQUITECTURA FINAL

Quiero una arquitectura profesional basada en Flask.

Website_D1/

│

├── app.py

├── conexion.py

├── config.py

│

├── routes/

│       dashboard.py

│       clientes.py

│       proveedores.py

│       productos.py

│       inventario.py

│       facturas.py

│       detalles_factura.py

│       ordenes.py

│       detalles_pedido.py

│       empleados.py

│       sedes.py

│       ciudades.py

│       categorias.py

│

├── models/

│       cliente.py

│       proveedor.py

│       producto.py

│       inventario.py

│       factura.py

│       detalle_factura.py

│       orden.py

│       detalle_pedido.py

│       empleado.py

│       sede.py

│       ciudad.py

│       categoria.py

│

├── templates/

│

│      base.html

│      navbar.html

│      sidebar.html

│      footer.html

│      index.html

│

│      dashboard/

│

│      clientes/

│

│      proveedores/

│

│      productos/

│

│      inventario/

│

│      facturas/

│

│      ordenes/

│

│      empleados/

│

│      sedes/

│

│      categorias/

│

├── static/

│      css/

│      js/

│      img/

│

├── utils/

│      pagination.py

│      validators.py

│      helpers.py

│      flash_messages.py

│

├── indices.sql

├── vistas.sql

└── requirements.txt

Puedes generar más archivos si son necesarios.

==========================================================

ANÁLISIS PREVIO

Antes de escribir cualquier archivo debes:

1.

Analizar completamente app.py.

2.

Analizar completamente conexion.py.

3.

Analizar completamente config.py.

4.

Analizar completamente Tablas.sql.

5.

Encontrar inconsistencias.

6.

Diseñar una arquitectura profesional.

7.

Explicar brevemente qué problemas encontraste.

NO escribas código antes de terminar ese análisis.

==========================================================

MODELS

Implementa una capa Models.

Cada modelo debe encargarse exclusivamente de acceder a PostgreSQL.

Las consultas SQL NO deben quedar dentro de las rutas.

Cada modelo debe contener:

Consultar

Consultar por ID

Insertar

Actualizar

Eliminar

cuando aplique.

==========================================================

ROUTES

Cada módulo debe tener su propio Blueprint.

Las rutas únicamente deben:

recibir solicitudes

validar datos

llamar al modelo correspondiente

renderizar templates

No deben contener SQL complejo.

==========================================================

TEMPLATES

Genera todos los templates necesarios.

Todos deben heredar de

base.html

Utilizar Bootstrap 5.

Diseño profesional.

Responsive.

Navbar superior.

Sidebar.

Breadcrumbs.

Tablas responsivas.

Mensajes Flash.

Botones consistentes.

Formularios limpios.

==========================================================

CRUD

Implementar CRUD para todas las entidades permitidas.

Consultar

Crear

Actualizar

Eliminar

==========================================================

REGLAS DEL NEGOCIO

CLIENTES

Permitir:

Consultar

Agregar

Editar

Eliminar

NO permitir eliminar clientes que tengan:

Facturas

Pedidos

Órdenes

asociadas.

==========================================================

PROVEEDORES

Permitir:

Consultar

Agregar

Editar

Eliminar

NO permitir eliminar proveedores que tengan:

Facturas

Órdenes

Pedidos

asociados.

==========================================================

PRODUCTOS

NO eliminar físicamente.

Implementar eliminación lógica.

Agregar un campo:

activo

Mostrar únicamente productos activos.

==========================================================

FACTURAS

Una factura emitida

NO puede editarse.

NO puede eliminarse.

Solo consultar.

==========================================================

ÓRDENES DE PEDIDO

Una orden confirmada

NO puede editarse.

NO puede eliminarse.

Solo consultar.

==========================================================

ACTUALIZACIONES

Permitir modificar únicamente datos generales.

No permitir modificar:

Número de factura

NIT

Documento

Identificadores históricos

cuando afecten la integridad.

==========================================================

PAGINACIÓN

Todas las tablas deben mostrar únicamente

100 registros por página.

Debe implementarse mediante SQL utilizando:

LIMIT

OFFSET

Debe existir:

Página actual

Total de páginas

Anterior

Siguiente

Total de registros

Nunca cargar todos los registros.

==========================================================

BUSCADORES

Todos los módulos deben tener buscador.

Clientes

Documento

Nombre

Correo

Teléfono

Proveedores

NIT

Nombre

Ciudad

Productos

Código

Nombre

Categoría

Proveedor

Inventario

Producto

Sede

Facturas

Número

Cliente

Empleado

Fecha

Órdenes

Proveedor

Estado

Fecha

etc.

==========================================================

ORDENAMIENTO

Permitir ordenar columnas.

Ascendente.

Descendente.

==========================================================

VALIDACIONES

Validar:

Campos obligatorios.

Duplicados.

Correos.

Teléfonos.

NIT.

Documentos.

Fechas.

Restricciones SQL.

Mostrar mensajes amigables utilizando Flask Flash.

==========================================================

CONSULTAS SQL

No utilizar SELECT *

Seleccionar únicamente columnas necesarias.

Utilizar JOIN correctamente.

Optimizar todas las consultas.

Reducir consultas innecesarias.

==========================================================

REQUISITOS ACADÉMICOS

Además del funcionamiento del Website, debes generar un archivo SQL llamado:

indices.sql

Creando índices en las tablas más consultadas para optimizar el rendimiento.

Explica brevemente el propósito de cada índice.

==========================================================

También debes generar un archivo llamado:

vistas.sql

Debe contener mínimo tres vistas empresariales.

Una vista debe calcular obligatoriamente:

Días de Stock

utilizando el inventario disponible y el consumo promedio.

Las otras dos deben responder a necesidades reales de una empresa tipo D1.

==========================================================

DOCUMENTACIÓN

Todo el código debe estar documentado.

Utilizar comentarios útiles.

Funciones pequeñas.

Código limpio.

Buenas prácticas de Python.

Buenas prácticas de Flask.

Buenas prácticas de PostgreSQL.

==========================================================

IMPORTANTE

NO quiero pseudocódigo.

NO quiero ejemplos.

NO quiero fragmentos.

Quiero archivos completos.

Cada archivo debe quedar listo para copiar y pegar.

Antes de generar un archivo verifica que sea completamente consistente con:

app.py

conexion.py

config.py

Tablas.sql

y con todos los archivos generados anteriormente.

==========================================================

FORMA DE ENTREGA

Como el proyecto es demasiado grande para una sola respuesta, debes desarrollarlo por fases.

FASE 1
- Analizar todos los archivos.
- Detectar errores e inconsistencias.
- Diseñar la arquitectura definitiva.
- Mostrar el árbol completo del proyecto final.
- Esperar mi confirmación antes de generar código.

FASE 2
- Generar app.py, conexion.py, config.py y requirements.txt completos.

FASE 3
- Generar todos los archivos de la carpeta models/.

FASE 4
- Generar todos los archivos de la carpeta routes/.

FASE 5
- Generar todos los archivos de la carpeta templates/, incluyendo base.html, navbar.html, sidebar.html y las vistas específicas de cada módulo.

FASE 6
- Generar los archivos de la carpeta static/ (CSS y JavaScript necesarios), así como los archivos de utils/.

FASE 7
- Generar indices.sql y vistas.sql.

FASE 8
- Realizar una auditoría final del proyecto, verificando que todas las rutas, modelos, templates y consultas sean coherentes con Tablas.sql y que el proyecto pueda ejecutarse correctamente con Flask y PostgreSQL sin requerir modificaciones adicionales.
```
