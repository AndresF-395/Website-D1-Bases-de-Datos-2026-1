import psycopg2
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
                    SELECT o.id_orden_pedido, o.fecha_pedido, o.estado_pedido, o.total, o.lugar_entrega,
                           p.nombre_proveedor, s.nombre_sede
                    FROM Ordenes_Pedidos o
                    INNER JOIN Proveedor p ON o.nit_proveedor = p.nit_proveedor
                    INNER JOIN Sedes s ON o.id_sede = s.id_sede
                """
                params = []

                if busqueda:
                    query += " WHERE p.nombre_proveedor ILIKE %s OR o.estado_pedido ILIKE %s"
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 2)

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
                    SELECT o.id_orden_pedido, o.fecha_pedido, o.estado_pedido, o.total, o.lugar_entrega,
                           o.nit_proveedor, p.nombre_proveedor, s.nombre_sede
                    FROM Ordenes_Pedidos o
                    INNER JOIN Proveedor p ON o.nit_proveedor = p.nit_proveedor
                    INNER JOIN Sedes s ON o.id_sede = s.id_sede
                """
                params = []
                if busqueda:
                    query += " WHERE p.nombre_proveedor ILIKE %s OR o.estado_pedido ILIKE %s"
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 2)
                
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
                    SELECT o.id_orden_pedido, o.fecha_pedido, o.estado_pedido, o.total, o.lugar_entrega,
                           o.nit_proveedor, p.nombre_proveedor, s.nombre_sede
                    FROM Ordenes_Pedidos o
                    INNER JOIN Proveedor p ON o.nit_proveedor = p.nit_proveedor
                    INNER JOIN Sedes s ON o.id_sede = s.id_sede
                    WHERE o.id_orden_pedido = %s
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
                query_orden = """
                    INSERT INTO Ordenes_Pedidos (nit_proveedor, id_sede, estado_pedido, total, lugar_entrega)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id_orden_pedido
                """
                cursor.execute(query_orden, (
                    datos_orden['nit_proveedor'], datos_orden['id_sede'], 
                    datos_orden.get('estado_pedido', 'PENDIENTE'), 
                    datos_orden['total'], datos_orden['lugar_entrega']
                ))
                id_orden = cursor.fetchone()[0]

                query_detalle = """
                    INSERT INTO Detalles_Pedidos (id_orden_pedido, id_producto, cantidad, 
                                                  precio_compra_unitario, subtotal_pedido)
                    VALUES (%s, %s, %s, %s, %s)
                """
                for det in lista_detalles:
                    cursor.execute(query_detalle, (
                        id_orden, det['id_producto'], det['cantidad'], 
                        det['precio_compra_unitario'], det['subtotal_pedido']
                    ))
                
                conexion.commit()
                return id_orden
        except Exception as e:
            conexion.rollback()
            raise e
        finally:
            conexion.close()