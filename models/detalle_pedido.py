import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class DetallePedidoModel:
    @staticmethod
    def obtener_por_orden(id_orden_pedido):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT dp.id_detalle_pedido, dp.cantidad, dp.precio_compra_unitario, 
                           dp.subtotal_pedido, p.nombre_producto, p.codigo_de_barras
                    FROM Detalles_Pedidos dp
                    INNER JOIN Productos p ON dp.id_producto = p.id_producto
                    WHERE dp.id_orden_pedido = %s
                """
                cursor.execute(query, (id_orden_pedido,))
                return cursor.fetchall()
        finally:
            conexion.close()