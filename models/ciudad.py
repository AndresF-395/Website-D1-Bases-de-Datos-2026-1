import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class CiudadModel:
    @staticmethod
    def obtener_todas():
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT id_ciudad, nombre_ciudad FROM Ciudad ORDER BY nombre_ciudad ASC")
                return cursor.fetchall()
        finally:
            conexion.close()