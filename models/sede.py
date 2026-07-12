import psycopg2
from psycopg2.extras import RealDictCursor
from conexion import conectar

class SedeModel:

    @staticmethod
    def obtener_todas():
        """Consulta optimizada para selectores (dropdowns) en otros formularios."""
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT id_sede, nombre_sede FROM Sedes ORDER BY nombre_sede ASC")
                return cursor.fetchall()
        finally:
            conexion.close()

    @staticmethod
    def obtener_paginados(limit=100, offset=0, busqueda=None, orden_columna='nombre_sede', orden_direccion='ASC'):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                columnas_validas = ['id_sede', 'nombre_sede', 'barrio_sede', 'direccion']
                if orden_columna not in columnas_validas:
                    orden_columna = 'nombre_sede'
                
                orden_direccion = 'DESC' if orden_direccion.upper() == 'DESC' else 'ASC'
                
                query = """
                    SELECT s.id_sede, s.nombre_sede, s.barrio_sede, s.direccion, 
                           s.horario_atencion_apertura, s.horario_atencion_cierre, c.nombre_ciudad
                    FROM Sedes s
                    INNER JOIN Ciudad c ON s.id_ciudad = c.id_ciudad
                """
                params = []

                if busqueda:
                    query += " WHERE s.nombre_sede ILIKE %s OR s.barrio_sede ILIKE %s OR c.nombre_ciudad ILIKE %s"
                    busqueda_param = f"%{busqueda}%"
                    params.extend([busqueda_param] * 3)

                query += f" ORDER BY {orden_columna} {orden_direccion} LIMIT %s OFFSET %s"
                params.extend([limit, offset])

                cursor.execute(query, tuple(params))
                return cursor.fetchall()
        finally:
            conexion.close()

    @staticmethod
    def obtener_por_id(id_sede):
        conexion = conectar()
        try:
            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT id_sede, nombre_sede, barrio_sede, id_ciudad, direccion, 
                           horario_atencion_apertura, horario_atencion_cierre
                    FROM Sedes
                    WHERE id_sede = %s
                """
                cursor.execute(query, (id_sede,))
                return cursor.fetchone()
        finally:
            conexion.close()