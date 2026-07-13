import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class ProductoModel:

    @staticmethod
    def obtener_paginados(limit=100, offset=0, busqueda=None, orden_columna='nombre_producto', orden_direccion='ASC'):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                columnas_validas = ['codigo_de_barras', 'nombre_producto', 'tipo_de_producto', 'precio_venta', 'marca']
                if orden_columna not in columnas_validas:
                    orden_columna = 'nombre_producto'
                
                orden_direccion = 'DESC' if orden_direccion.upper() == 'DESC' else 'ASC'
                
                # Se filtra por activo = TRUE según regla de negocio
                query = """
                    SELECT p.id_producto, p.codigo_de_barras, p.nombre_producto, p.tipo_de_producto, 
                           p.precio_compra, p.precio_venta, p.marca, p.tipo_iva, p.demanda_diaria,
                           p.activo, ppp.nit_proveedor, pr.nombre_proveedor
                    FROM Productos p
                    LEFT JOIN Productos_Por_Proveedor ppp
                        ON p.id_producto = ppp.codigo_producto
                       AND ppp.activo = TRUE
                    LEFT JOIN Proveedor pr
                        ON ppp.nit_proveedor = pr.nit_proveedor
                    WHERE p.activo = TRUE
                """
                params = []

                if busqueda:
                    query += " AND (codigo_de_barras ILIKE %s OR nombre_producto ILIKE %s OR marca ILIKE %s OR tipo_de_producto ILIKE %s)"
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 4)

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
                query = "SELECT COUNT(id_producto) FROM Productos WHERE activo = TRUE"
                params = []
                if busqueda:
                    query += " AND (codigo_de_barras ILIKE %s OR nombre_producto ILIKE %s OR marca ILIKE %s)"
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 3)
                
                cursor.execute(query, tuple(params))
                return cursor.fetchone()[0]
        finally:
            conexion.close()

    @staticmethod
    def obtener_por_id(id_producto):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT 
                        p.id_producto,
                        p.codigo_de_barras,
                        p.nombre_producto,
                        p.tipo_de_producto,
                        p.precio_compra,
                        p.precio_venta,
                        p.marca,
                        p.fecha_vencimiento,
                        p.tipo_iva,
                        p.activo,
                        p.demanda_diaria,
                        ppp.nit_proveedor
                    FROM Productos p
                    LEFT JOIN Productos_Por_Proveedor ppp
                        ON p.id_producto = ppp.codigo_producto
                       AND ppp.activo = TRUE
                    WHERE p.id_producto = %s AND p.activo = TRUE
                """
                cursor.execute(query, (id_producto,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def crear(datos):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                query = """
                    INSERT INTO Productos (codigo_de_barras, nombre_producto, tipo_de_producto, precio_compra, 
                                           precio_venta, marca, fecha_vencimiento, tipo_iva, demanda_diaria)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_producto
                """
                cursor.execute(query, (
                    datos['codigo_de_barras'], datos['nombre_producto'], datos['tipo_de_producto'], 
                    datos['precio_compra'], datos['precio_venta'], datos['marca'], 
                    datos.get('fecha_vencimiento'), datos['tipo_iva'], datos.get('demanda_diaria', 0)
                ))
                id_producto = cursor.fetchone()[0]
                cursor.execute(
                    """
                    INSERT INTO Productos_Por_Proveedor (nit_proveedor, codigo_producto, precio_compra)
                    VALUES (%s, %s, %s)
                    """,
                    (datos['nit_proveedor'], id_producto, datos['precio_compra'])
                )
                conexion.commit()
                return id_producto
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def actualizar(id_producto, datos):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                query = """
                    UPDATE Productos
                    SET nombre_producto = %s, tipo_de_producto = %s, precio_compra = %s, 
                        precio_venta = %s, marca = %s, fecha_vencimiento = %s, tipo_iva = %s, 
                        demanda_diaria = %s
                    WHERE id_producto = %s AND activo = TRUE
                """
                cursor.execute(query, (
                    datos['nombre_producto'], datos['tipo_de_producto'], datos['precio_compra'], 
                    datos['precio_venta'], datos['marca'], datos.get('fecha_vencimiento'), 
                    datos['tipo_iva'], datos.get('demanda_diaria', 0), id_producto
                ))
                actualizado = cursor.rowcount > 0
                cursor.execute(
                    """
                    UPDATE Productos_Por_Proveedor
                    SET activo = FALSE, fecha_fin_suministro = CURRENT_DATE
                    WHERE codigo_producto = %s AND activo = TRUE
                    """,
                    (id_producto,)
                )
                cursor.execute(
                    """
                    INSERT INTO Productos_Por_Proveedor (nit_proveedor, codigo_producto, precio_compra)
                    VALUES (%s, %s, %s)
                    """,
                    (datos['nit_proveedor'], id_producto, datos['precio_compra'])
                )
                conexion.commit()
                return actualizado
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    @staticmethod
    def eliminar_logico(id_producto):
        """Implementa la eliminación lógica cambiando activo a FALSE."""
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                query = "UPDATE Productos SET activo = FALSE WHERE id_producto = %s"
                cursor.execute(query, (id_producto,))
                conexion.commit()
                return cursor.rowcount > 0
        finally:
            conexion.close()
