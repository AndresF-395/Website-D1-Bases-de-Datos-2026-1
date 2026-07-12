import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class InventarioModel:

    @staticmethod
    def obtener_paginados(limit=100, offset=0, busqueda=None, orden_columna='id_inventario', orden_direccion='ASC'):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                columnas_validas = ['id_inventario', 'cantidad_disponible', 'stock_minimo', 'stock_maximo']
                if orden_columna not in columnas_validas:
                    orden_columna = 'id_inventario'
                
                orden_direccion = 'DESC' if orden_direccion.upper() == 'DESC' else 'ASC'
                
                query = """
                    SELECT i.id_inventario, i.cantidad_disponible, i.stock_minimo, i.stock_maximo,
                           p.nombre_producto, p.codigo_de_barras, p.demanda_diaria, s.nombre_sede
                    FROM Inventario i
                    INNER JOIN Productos p ON i.id_producto = p.id_producto
                    INNER JOIN Sedes s ON i.id_sede = s.id_sede
                """
                params = []

                if busqueda:
                    query += " WHERE p.nombre_producto ILIKE %s OR s.nombre_sede ILIKE %s OR p.codigo_de_barras ILIKE %s"
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 3)

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
                    SELECT COUNT(i.id_inventario) 
                    FROM Inventario i
                    INNER JOIN Productos p ON i.id_producto = p.id_producto
                    INNER JOIN Sedes s ON i.id_sede = s.id_sede
                """
                params = []
                if busqueda:
                    query += " WHERE p.nombre_producto ILIKE %s OR s.nombre_sede ILIKE %s"
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 2)
                
                cursor.execute(query, tuple(params))
                return cursor.fetchone()[0]
        finally:
            conexion.close()

    @staticmethod
    def obtener_por_id(id_inventario):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT i.id_inventario, i.id_producto, i.id_sede, i.cantidad_disponible, 
                           i.stock_minimo, i.stock_maximo
                    FROM Inventario i
                    WHERE i.id_inventario = %s
                """
                cursor.execute(query, (id_inventario,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def crear(datos):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                query = """
                    INSERT INTO Inventario (id_producto, id_sede, cantidad_disponible, stock_minimo, stock_maximo)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id_inventario
                """
                cursor.execute(query, (
                    datos['id_producto'], datos['id_sede'], datos.get('cantidad_disponible', 0), 
                    datos.get('stock_minimo', 10), datos.get('stock_maximo', 1000)
                ))
                conexion.commit()
                return cursor.fetchone()[0]
        finally:
            conexion.close()

    @staticmethod
    def actualizar(id_inventario, datos):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                query = """
                    UPDATE Inventario
                    SET id_producto = %s, id_sede = %s, cantidad_disponible = %s, 
                        stock_minimo = %s, stock_maximo = %s
                    WHERE id_inventario = %s
                """
                cursor.execute(query, (
                    datos['id_producto'], datos['id_sede'], datos['cantidad_disponible'], 
                    datos['stock_minimo'], datos['stock_maximo'], id_inventario
                ))
                conexion.commit()
                return cursor.rowcount > 0
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_inventario):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM Inventario WHERE id_inventario = %s", (id_inventario,))
                conexion.commit()
                return cursor.rowcount > 0
        finally:
            conexion.close()