import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class FacturaModel:

    @staticmethod
    def obtener_datos_pos():
        """Obtiene datos iniciales filtrados para el Punto de Venta (POS)."""
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                # 1. Sedes
                cursor.execute("SELECT id_sede, nombre_sede FROM Sedes ORDER BY nombre_sede;")
                sedes = cursor.fetchall()
                
                # 2. Clientes
                cursor.execute("SELECT id_cliente, nombres, apellidos, numero_documento FROM Cliente ORDER BY nombres;")
                clientes = cursor.fetchall()
                
                # 3. Empleados vinculados a su sede
                cursor.execute("SELECT id_empleado, nombre_empleado, apellido_empleado, id_sede FROM Empleados;")
                empleados = cursor.fetchall()
                
                # 4. Inventario cruzado con Productos para saber stock exacto por sede
                query_inv = """
                    SELECT i.id_sede, i.id_producto, p.nombre_producto, p.codigo_de_barras, 
                           i.cantidad_disponible, p.precio_venta, p.tipo_iva
                    FROM Inventario i
                    INNER JOIN Productos p ON i.id_producto = p.id_producto
                    WHERE i.cantidad_disponible > 0 AND p.activo = TRUE;
                """
                cursor.execute(query_inv)
                inventario = cursor.fetchall()
                
                return sedes, clientes, empleados, inventario
        finally:
            conexion.close()
    
    @staticmethod
    def obtener_paginados(limit=100, offset=0, busqueda=None, orden_columna='fecha_emision', orden_direccion='DESC'):
        """Retorna el registro de facturas sin posibilidad de edición posterior."""
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                columnas_validas = ['id_factura', 'numero_factura_oficial', 'fecha_emision', 'total_factura']
                if orden_columna not in columnas_validas:
                    orden_columna = 'fecha_emision'
                
                orden_direccion = 'DESC' if orden_direccion.upper() == 'DESC' else 'ASC'
                
                # JOIN para optimizar lecturas y no traer IDs sueltos
                query = """
                    SELECT f.id_factura, f.numero_factura_oficial, f.fecha_emision, f.forma_pago, f.total_factura,
                           c.nombres || ' ' || c.apellidos AS cliente_nombre,
                           c.numero_documento,
                           s.nombre_sede,
                           e.nombre_empleado || ' ' || e.apellido_empleado AS empleado_nombre
                    FROM Factura f
                    INNER JOIN Cliente c ON f.id_cliente = c.id_cliente
                    INNER JOIN Sedes s ON f.id_sede = s.id_sede
                    INNER JOIN Empleados e ON f.id_empleado = e.id_empleado
                """
                params = []

                if busqueda:
                    query += """
                        WHERE f.numero_factura_oficial ILIKE %s 
                           OR c.numero_documento ILIKE %s 
                           OR c.nombres ILIKE %s
                    """
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
                    SELECT COUNT(f.id_factura) 
                    FROM Factura f
                    INNER JOIN Cliente c ON f.id_cliente = c.id_cliente
                """
                params = []
                if busqueda:
                    query += " WHERE f.numero_factura_oficial ILIKE %s OR c.numero_documento ILIKE %s OR c.nombres ILIKE %s"
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 3)
                
                cursor.execute(query, tuple(params))
                return cursor.fetchone()[0]
        finally:
            conexion.close()

    @staticmethod
    def obtener_por_id(id_factura):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT f.id_factura, f.numero_factura_oficial, f.id_cliente, f.id_sede, f.id_empleado,
                           f.fecha_emision, f.forma_pago, f.subtotal, f.total_iva, f.total_descuento,
                           f.total_factura, f.valor_pagado, f.cambio_devuelto,
                           c.nombres || ' ' || c.apellidos AS cliente_nombre,
                           c.numero_documento AS cliente_documento,
                           c.telefono_cliente,
                           s.nombre_sede,
                           e.nombre_empleado || ' ' || e.apellido_empleado AS empleado_nombre
                    FROM Factura f
                    INNER JOIN Cliente c ON f.id_cliente = c.id_cliente
                    INNER JOIN Sedes s ON f.id_sede = s.id_sede
                    INNER JOIN Empleados e ON f.id_empleado = e.id_empleado
                    WHERE f.id_factura = %s
                """
                cursor.execute(query, (id_factura,))
                return cursor.fetchone()
        finally:
            conexion.close()
            
    @staticmethod
    def crear_con_detalles(datos_factura, lista_detalles):
        """
        Inserta la factura y sus detalles dentro de una sola transacción.
        El Trigger fx_actualizar_inventario_venta actuará al insertar en Detalle_Factura.
        """
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                # 1. Insertar Factura
                query_factura = """
                    INSERT INTO Factura (numero_factura_oficial, id_cliente, id_sede, id_empleado, 
                                         forma_pago, subtotal, total_iva, total_descuento, 
                                         total_factura, valor_pagado, cambio_devuelto)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_factura
                """
                cursor.execute(query_factura, (
                    datos_factura['numero_factura_oficial'], datos_factura['id_cliente'],
                    datos_factura['id_sede'], datos_factura['id_empleado'], datos_factura['forma_pago'],
                    datos_factura['subtotal'], datos_factura['total_iva'], datos_factura['total_descuento'],
                    datos_factura['total_factura'], datos_factura['valor_pagado'], datos_factura['cambio_devuelto']
                ))
                id_factura = cursor.fetchone()[0]

                # 2. Insertar Detalles
                query_detalle = """
                    INSERT INTO Detalle_Factura (id_factura, id_producto, cantidad, 
                                                 precio_unitario_aplicado, subtotal_linea, iva_aplicado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                for det in lista_detalles:
                    cursor.execute(query_detalle, (
                        id_factura, det['id_producto'], det['cantidad'], 
                        det['precio_unitario_aplicado'], det['subtotal_linea'], det['iva_aplicado']
                    ))
                
                # Solo si ambas inserciones son exitosas, confirmamos.
                conexion.commit()
                return id_factura
        except Exception as e:
            conexion.rollback()
            raise e
        finally:
            conexion.close()