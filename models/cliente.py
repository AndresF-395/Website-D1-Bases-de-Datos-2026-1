import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class ClienteModel:
    
    @staticmethod
    def obtener_paginados(limit=100, offset=0, busqueda=None, orden_columna='id_cliente', orden_direccion='ASC'):
        """Retorna clientes con paginación, búsqueda y ordenamiento dinámico."""
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                # Whitelist de columnas para evitar inyección SQL en el ORDER BY
                columnas_validas = ['id_cliente', 'tipo_documento', 'numero_documento', 'nombres', 'apellidos', 'correo_cliente', 'telefono_cliente']
                if orden_columna not in columnas_validas:
                    orden_columna = 'id_cliente'
                
                orden_direccion = 'DESC' if orden_direccion.upper() == 'DESC' else 'ASC'
                
                query = """
                    SELECT id_cliente, tipo_documento, numero_documento, nombres, apellidos, 
                           telefono_cliente, correo_cliente, direccion_residencia, habeas_data
                    FROM Cliente
                """
                params = []

                if busqueda:
                    query += """
                        WHERE numero_documento ILIKE %s 
                           OR nombres ILIKE %s 
                           OR apellidos ILIKE %s 
                           OR correo_cliente ILIKE %s 
                           OR telefono_cliente ILIKE %s
                    """
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 5)

                query += f" ORDER BY {orden_columna} {orden_direccion} LIMIT %s OFFSET %s"
                params.extend([limit, offset])

                cursor.execute(query, tuple(params))
                return cursor.fetchall()
        finally:
            conexion.close()

    @staticmethod
    def contar_total(busqueda=None):
        """Cuenta el total de registros para calcular las páginas en la UI."""
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                query = "SELECT COUNT(id_cliente) FROM Cliente"
                params = []
                if busqueda:
                    query += """
                        WHERE numero_documento ILIKE %s 
                           OR nombres ILIKE %s 
                           OR apellidos ILIKE %s 
                           OR correo_cliente ILIKE %s 
                           OR telefono_cliente ILIKE %s
                    """
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 5)
                
                cursor.execute(query, tuple(params))
                return cursor.fetchone()[0]
        finally:
            conexion.close()

    @staticmethod
    def obtener_por_id(id_cliente):
        """Consulta un cliente específico por su ID."""
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT id_cliente, tipo_documento, numero_documento, nombres, apellidos, 
                           telefono_cliente, correo_cliente, direccion_residencia, habeas_data
                    FROM Cliente
                    WHERE id_cliente = %s
                """
                cursor.execute(query, (id_cliente,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def crear(datos):
        """Inserta un nuevo cliente."""
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                query = """
                    INSERT INTO Cliente (tipo_documento, numero_documento, nombres, apellidos, 
                                         telefono_cliente, correo_cliente, direccion_residencia, habeas_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_cliente
                """
                cursor.execute(query, (
                    datos['tipo_documento'], datos['numero_documento'], datos['nombres'], 
                    datos['apellidos'], datos['telefono_cliente'], datos['correo_cliente'], 
                    datos['direccion_residencia'], datos['habeas_data']
                ))
                conexion.commit()
                return cursor.fetchone()[0]
        finally:
            conexion.close()

    @staticmethod
    def actualizar(id_cliente, datos):
        """Actualiza datos generales. La validación de NO modificar documento se maneja en el controlador."""
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                query = """
                    UPDATE Cliente
                    SET nombres = %s, apellidos = %s, telefono_cliente = %s, 
                        correo_cliente = %s, direccion_residencia = %s, habeas_data = %s
                    WHERE id_cliente = %s
                """
                cursor.execute(query, (
                    datos['nombres'], datos['apellidos'], datos['telefono_cliente'], 
                    datos['correo_cliente'], datos['direccion_residencia'], 
                    datos['habeas_data'], id_cliente
                ))
                conexion.commit()
                return cursor.rowcount > 0
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_cliente):
        """
        Intenta eliminar un cliente. 
        Retorna True si es exitoso, lanza ValueError si viola integridad referencial.
        """
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM Cliente WHERE id_cliente = %s", (id_cliente,))
                conexion.commit()
                return cursor.rowcount > 0
        except psycopg2.IntegrityError:
            conexion.rollback()
            raise ValueError("No se puede eliminar el cliente porque tiene facturas u otros registros asociados.")
        finally:
            conexion.close()