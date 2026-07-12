import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class DepartamentoModel:
    @staticmethod
    def obtener_todos():
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT id_departamento, nombre_departamento FROM Departamentos ORDER BY nombre_departamento ASC")
                return cursor.fetchall()
        finally:
            conexion.close()