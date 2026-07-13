import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class EmpleadoModel:

    @staticmethod
    def obtener_paginados(limit=100, offset=0, busqueda=None, orden_columna='id_empleado', orden_direccion='ASC'):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                columnas_validas = ['id_empleado', 'cedula_empleado', 'nombre_empleado', 'apellido_empleado', 'cargo', 'salario']
                if orden_columna not in columnas_validas:
                    orden_columna = 'id_empleado'
                
                orden_direccion = 'DESC' if orden_direccion.upper() == 'DESC' else 'ASC'
                
                query = """
                    SELECT e.id_empleado, e.cedula_empleado, e.nombre_empleado, e.apellido_empleado, 
                           e.cargo, e.salario, e.telefono_empleado, e.correo_empleado, s.nombre_sede
                    FROM Empleados e
                    INNER JOIN Sedes s ON e.id_sede = s.id_sede
                """
                params = []

                if busqueda:
                    query += " WHERE e.cedula_empleado ILIKE %s OR e.nombre_empleado ILIKE %s OR e.apellido_empleado ILIKE %s"
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
                query = "SELECT COUNT(id_empleado) FROM Empleados"
                params = []
                if busqueda:
                    query += " WHERE cedula_empleado ILIKE %s OR nombre_empleado ILIKE %s OR apellido_empleado ILIKE %s"
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 3)
                
                cursor.execute(query, tuple(params))
                return cursor.fetchone()[0]
        finally:
            conexion.close()

    @staticmethod
    def obtener_por_id(id_empleado):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT id_empleado, cedula_empleado, nombre_empleado, apellido_empleado, 
                           fecha_nacimiento, cargo, salario, fecha_contrato, telefono_empleado, 
                           correo_empleado, id_sede
                    FROM Empleados
                    WHERE id_empleado = %s
                """
                cursor.execute(query, (id_empleado,))
                return cursor.fetchone()
        finally:
            conexion.close()

    @staticmethod
    def crear(datos):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                query = """
                    INSERT INTO Empleados (cedula_empleado, nombre_empleado, apellido_empleado, 
                                           fecha_nacimiento, cargo, salario, fecha_contrato, 
                                           telefono_empleado, correo_empleado, id_sede)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_empleado
                """
                cursor.execute(query, (
                    datos['cedula_empleado'], datos['nombre_empleado'], datos['apellido_empleado'], 
                    datos['fecha_nacimiento'], datos['cargo'], datos['salario'], 
                    datos.get('fecha_contrato'), datos['telefono_empleado'], 
                    datos['correo_empleado'], datos['id_sede']
                ))
                conexion.commit()
                return cursor.fetchone()[0]
        except psycopg2.IntegrityError as e:
            conexion.rollback()
            raise ValueError(f"Error de integridad: {str(e)}")
        finally:
            conexion.close()

    @staticmethod
    def actualizar(id_empleado, datos):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                # No se actualiza la cédula por integridad
                query = """
                    UPDATE Empleados
                    SET nombre_empleado = %s, apellido_empleado = %s, fecha_nacimiento = %s, 
                        cargo = %s, salario = %s, fecha_contrato = %s, telefono_empleado = %s, 
                        correo_empleado = %s, id_sede = %s
                    WHERE id_empleado = %s
                """
                cursor.execute(query, (
                    datos['nombre_empleado'], datos['apellido_empleado'], datos['fecha_nacimiento'], 
                    datos['cargo'], datos['salario'], datos['fecha_contrato'], 
                    datos['telefono_empleado'], datos['correo_empleado'], datos['id_sede'], id_empleado
                ))
                conexion.commit()
                return cursor.rowcount > 0
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_empleado):
        conexion = conectar()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM Empleados WHERE id_empleado = %s", (id_empleado,))
                conexion.commit()
                return cursor.rowcount > 0
        except psycopg2.IntegrityError:
            conexion.rollback()
            raise ValueError("No se puede eliminar el empleado porque tiene facturas o turnos asociados.")
        finally:
            conexion.close()
    @staticmethod
    def obtener_por_sede(id_sede):
        """Recupera todos los empleados asignados a una sede específica."""
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT id_empleado, cedula_empleado, nombre_empleado, apellido_empleado, 
                           cargo, telefono_empleado, correo_empleado, salario
                    FROM Empleados
                    WHERE id_sede = %s
                    ORDER BY nombre_empleado ASC
                """
                cursor.execute(query, (id_sede,))
                return cursor.fetchall()
        finally:
            conexion.close()