import mysql.connector
from mysql.connector import Error

# Configuración de credenciales
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # Cambiar si tu usuario es diferente
    'password': '',          # Cambiar si tienes contraseña en XAMPP/MySQL
    'database': 'd1_db'      # Asegurar que coincida con la fase 1
}

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos MySQL.
    Utiliza dictionary=True para que las consultas devuelvan diccionarios en lugar de tuplas.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def execute_query(query, params=None, fetch=True):
    """
    Función de utilidad para ejecutar consultas SELECT, INSERT, UPDATE o DELETE.
    """
    connection = get_db_connection()
    if not connection:
        return None

    try:
        # dictionary=True es crucial para que Jinja iteré por nombre de columna (ej: cliente.nombres)
        cursor = connection.cursor(dictionary=True) 
        cursor.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            if fetch:
                result = cursor.fetchall()
                return result
        else:
            connection.commit()
            return cursor.lastrowid
            
    except Error as e:
        print(f"Error ejecutando consulta: {e}")
        connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()