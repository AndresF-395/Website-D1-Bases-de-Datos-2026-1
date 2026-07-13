
from psycopg2.extras import RealDictCursor
from conexion import conectar


class OrdenModel:

    @staticmethod
    def obtener_paginados(limit=100, offset=0, busqueda=None, orden_columna='fecha_pedido', orden_direccion='DESC'):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:

                columnas_validas = ['id_orden_pedido', 'fecha_pedido', 'estado_pedido', 'total']

                if orden_columna not in columnas_validas:
                    orden_columna = 'fecha_pedido'

                orden_direccion = 'DESC' if orden_direccion.upper() == 'DESC' else 'ASC'

                query = """
                    SELECT
                        o.id_orden_pedido,
                        o.fecha_pedido,
                        o.estado_pedido,
                        COALESCE(SUM(dp.subtotal_pedido),0) AS total,
                        o.lugar_entrega,
                        o.nit_proveedor,
                        p.nombre_proveedor,
                        s.nombre_sede
                    FROM Ordenes_Pedidos o
                    INNER JOIN Proveedor p
                        ON o.nit_proveedor = p.nit_proveedor
                    INNER JOIN Sedes s
                        ON o.id_sede = s.id_sede
                    LEFT JOIN Detalles_Pedidos dp
                        ON o.id_orden_pedido = dp.id_orden_pedido
                """

                params = []

                if busqueda:
                    query += """
                        WHERE p.nombre_proveedor ILIKE %s
                        OR o.estado_pedido ILIKE %s
                        OR o.nit_proveedor ILIKE %s
                    """

                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 3)

                query += """
                    GROUP BY
                        o.id_orden_pedido,
                        o.fecha_pedido,
                        o.estado_pedido,
                        o.lugar_entrega,
                        o.nit_proveedor,
                        p.nombre_proveedor,
                        s.nombre_sede
                """

                query += f" ORDER BY {orden_columna} {orden_direccion} LIMIT %s OFFSET %s"

                params.extend([limit, offset])

                cursor.execute(query, tuple(params))
                return cursor.fetchall()

        finally:
            conexion.close()
    @staticmethod
    def contar_total(busqueda=None):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:

                query = """
                    SELECT COUNT(o.id_orden_pedido)
                    FROM Ordenes_Pedidos o
                    INNER JOIN Proveedor p
                        ON o.nit_proveedor = p.nit_proveedor
                """

                params = []

                if busqueda:
                    query += """
                        WHERE p.nombre_proveedor ILIKE %s
                           OR o.estado_pedido ILIKE %s
                           OR o.nit_proveedor ILIKE %s
                    """

                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 3)

                cursor.execute(query, tuple(params))

                return cursor.fetchone()[0]

        finally:
            conexion.close()      
    @staticmethod
    def obtener_por_id(id_orden_pedido):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                         SELECT 
                            o.id_orden_pedido,
                            o.fecha_pedido,
                            o.estado_pedido,
                            COALESCE(SUM(dp.subtotal_pedido),0) AS total,
                            o.lugar_entrega,
                            o.nit_proveedor,
                            p.nombre_proveedor,
                            s.nombre_sede
                        FROM Ordenes_Pedidos o
                        INNER JOIN Proveedor p 
                            ON o.nit_proveedor = p.nit_proveedor
                        INNER JOIN Sedes s 
                            ON o.id_sede = s.id_sede
                        LEFT JOIN Detalles_Pedidos dp 
                            ON o.id_orden_pedido = dp.id_orden_pedido
                        WHERE o.id_orden_pedido = %s
                        GROUP BY 
                            o.id_orden_pedido,
                            o.fecha_pedido,
                            o.estado_pedido,
                            o.lugar_entrega,
                            o.nit_proveedor,
                            p.nombre_proveedor,
                            s.nombre_sede
                         """
                cursor.execute(query, (id_orden_pedido,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def crear_con_detalles(datos_orden, lista_detalles):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                if datos_orden.get('fecha_pedido'):
                    cursor.execute(
                        """
                        INSERT INTO Ordenes_Pedidos (nit_proveedor, id_sede, fecha_pedido, estado_pedido, total, lugar_entrega)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_orden_pedido
                        """,
                        (
                            datos_orden['nit_proveedor'], datos_orden['id_sede'], datos_orden['fecha_pedido'],
                            datos_orden.get('estado_pedido', 'PENDIENTE'), datos_orden['total'],
                            datos_orden['lugar_entrega']
                        )
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO Ordenes_Pedidos (nit_proveedor, id_sede, estado_pedido, total, lugar_entrega)
                        VALUES (%s, %s, %s, %s, %s) RETURNING id_orden_pedido
                        """,
                        (
                            datos_orden['nit_proveedor'], datos_orden['id_sede'],
                            datos_orden.get('estado_pedido', 'PENDIENTE'), datos_orden['total'],
                            datos_orden['lugar_entrega']
                        )
                    )

                id_orden = cursor.fetchone()[0]

                for det in lista_detalles:
                    cursor.execute(
                        """
                        INSERT INTO Detalles_Pedidos (id_orden_pedido, id_producto, cantidad,
                                                      precio_compra_unitario, subtotal_pedido)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            id_orden, det['id_producto'], det['cantidad'],
                            det['precio_compra_unitario'], det['subtotal_pedido']
                        )
                    )
    
                conexion.commit()
                return id_orden
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def obtener_datos_pedido():
        """Obtiene sedes, proveedores, empleados y el catálogo cruzado con la tabla intermedia y el stock."""
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT id_sede, nombre_sede FROM Sedes ORDER BY nombre_sede;")
                sedes = cursor.fetchall()
                
                cursor.execute("SELECT nit_proveedor, nombre_proveedor FROM Proveedor ORDER BY nombre_proveedor;")
                proveedores = cursor.fetchall()
                
                cursor.execute("SELECT id_empleado, nombre_empleado, apellido_empleado, id_sede FROM Empleados;")
                empleados = cursor.fetchall()
                
                # Cruce maestro: Productos vinculados al proveedor, cruzados con todas las sedes
                query_productos = """
                    SELECT p.id_producto, p.nombre_producto, p.codigo_de_barras, 
                           pp.precio_compra, pp.nit_proveedor,
                           s.id_sede, COALESCE(i.cantidad_disponible, 0) AS stock_sede
                    FROM Productos p
                    INNER JOIN Productos_Por_Proveedor pp ON p.id_producto = pp.codigo_producto
                    CROSS JOIN Sedes s
                    LEFT JOIN Inventario i ON p.id_producto = i.id_producto AND s.id_sede = i.id_sede
                    WHERE p.activo = TRUE AND pp.activo = TRUE
                    ORDER BY p.nombre_producto;
                """
                cursor.execute(query_productos)
                productos_inventario = cursor.fetchall()
                
                return sedes, proveedores, empleados, productos_inventario
        finally:
            conexion.close()