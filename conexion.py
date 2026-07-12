import psycopg2
from psycopg2 import OperationalError
from config import Config

def conectar():
    """
    Establece y retorna una conexión a la base de datos PostgreSQL.
    
    Toda operación sobre la base de datos DEBE utilizar esta función.
    Es responsabilidad de los Modelos (capa models/) gestionar la creación
    de cursores (cursor()), la confirmación de transacciones (commit())
    y el cierre seguro de la conexión (close()).
    """
    try:
        conexion = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        return conexion
    except OperationalError as e:
        # Aquí se registraría el error en un log empresarial en producción
        print(f"Error Crítico: No se pudo conectar a la base de datos PostgreSQL. Detalle: {e}")
        raise e