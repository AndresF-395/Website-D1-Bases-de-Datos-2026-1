import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class DetalleFacturaModel:
    @staticmethod
    def obtener_por_factura(id_factura):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT df.id_linea, df.cantidad, df.precio_unitario_aplicado, 
                           df.subtotal_linea, df.iva_aplicado, p.nombre_producto, p.codigo_de_barras
                    FROM Detalle_Factura df
                    INNER JOIN Productos p ON df.id_producto = p.id_producto
                    WHERE df.id_factura = %s
                """
                cursor.execute(query, (id_factura,))
                return cursor.fetchall()
        finally:
            conexion.close()