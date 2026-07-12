import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class ProveedorModel:
    
    @staticmethod
    def obtener_paginados(limit=100, offset=0, busqueda=None, orden_columna='nombre_proveedor', orden_direccion='ASC'):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                columnas_validas = ['nit_proveedor', 'nombre_proveedor', 'telefono_proveedor', 'correo_proveedor', 'calificacion']
                if orden_columna not in columnas_validas:
                    orden_columna = 'nombre_proveedor'
                
                orden_direccion = 'DESC' if orden_direccion.upper() == 'DESC' else 'ASC'
                
                query = """
                    SELECT nit_proveedor, nombre_proveedor, direccion_empresa, telefono_proveedor, 
                           correo_proveedor, rut, tipo_proveedor, tiempo_entrega_promedio, calificacion
                    FROM Proveedor
                """
                params = []

                if busqueda:
                    query += """
                        WHERE nit_proveedor ILIKE %s 
                           OR nombre_proveedor ILIKE %s 
                           OR correo_proveedor ILIKE %s
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
                query = "SELECT COUNT(nit_proveedor) FROM Proveedor"
                params = []
                if busqueda:
                    query += " WHERE nit_proveedor ILIKE %s OR nombre_proveedor ILIKE %s OR correo_proveedor ILIKE %s"
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 3)
                
                cursor.execute(query, tuple(params))
                return cursor.fetchone()[0]
        finally:
            conexion.close()

    @staticmethod
    def obtener_por_nit(nit_proveedor):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT nit_proveedor, nombre_proveedor, direccion_empresa, telefono_proveedor, 
                           correo_proveedor, rut, certificacion_bancaria, tipo_proveedor, 
                           tiempo_entrega_promedio, contacto_comercial, contacto_cartera, 
                           contacto_logistico, condiciones_pago, calificacion
                    FROM Proveedor
                    WHERE nit_proveedor = %s
                """
                cursor.execute(query, (nit_proveedor,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def crear(datos):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                # Convertir strings vacíos de HTML a None o a valores por defecto para evitar errores de tipo en BD
                rut = datos.get('rut') if datos.get('rut') else None
                tiempo_entrega = datos.get('tiempo_entrega_promedio') if datos.get('tiempo_entrega_promedio') else 0
                calificacion = datos.get('calificacion') if datos.get('calificacion') else 5

                query = """
                    INSERT INTO Proveedor (nit_proveedor, nombre_proveedor, direccion_empresa, telefono_proveedor, 
                                           correo_proveedor, rut, certificacion_bancaria, tipo_proveedor, 
                                           tiempo_entrega_promedio, contacto_comercial, contacto_cartera, 
                                           contacto_logistico, condiciones_pago, calificacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    datos['nit_proveedor'], datos['nombre_proveedor'], datos.get('direccion_empresa'), 
                    datos.get('telefono_proveedor'), datos.get('correo_proveedor'), rut, 
                    datos.get('certificacion_bancaria'), datos.get('tipo_proveedor'), tiempo_entrega, 
                    datos.get('contacto_comercial'), datos.get('contacto_cartera'), datos.get('contacto_logistico'), 
                    datos.get('condiciones_pago'), calificacion
                ))
                conexion.commit()
                return True
        finally:
            conexion.close()

    @staticmethod
    def actualizar(nit_proveedor, datos):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                tiempo_entrega = datos.get('tiempo_entrega_promedio') if datos.get('tiempo_entrega_promedio') else 0
                calificacion = datos.get('calificacion') if datos.get('calificacion') else 5

                query = """
                    UPDATE Proveedor
                    SET nombre_proveedor = %s, direccion_empresa = %s, telefono_proveedor = %s, 
                        correo_proveedor = %s, certificacion_bancaria = %s, tipo_proveedor = %s, 
                        tiempo_entrega_promedio = %s, contacto_comercial = %s, contacto_cartera = %s, 
                        contacto_logistico = %s, condiciones_pago = %s, calificacion = %s
                    WHERE nit_proveedor = %s
                """
                cursor.execute(query, (
                    datos['nombre_proveedor'], datos.get('direccion_empresa'), datos.get('telefono_proveedor'), 
                    datos.get('correo_proveedor'), datos.get('certificacion_bancaria'), datos.get('tipo_proveedor'), 
                    tiempo_entrega, datos.get('contacto_comercial'), datos.get('contacto_cartera'), 
                    datos.get('contacto_logistico'), datos.get('condiciones_pago'), calificacion, 
                    nit_proveedor
                ))
                conexion.commit()
                return cursor.rowcount > 0
        finally:
            conexion.close()

    @staticmethod
    def eliminar(nit_proveedor):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM Proveedor WHERE nit_proveedor = %s", (nit_proveedor,))
                conexion.commit()
                return cursor.rowcount > 0
        except psycopg2.IntegrityError:
            conexion.rollback()
            raise ValueError("No se puede eliminar el proveedor porque tiene órdenes de pedido o registros asociados.")
        finally:
            conexion.close()