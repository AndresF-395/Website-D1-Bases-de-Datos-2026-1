import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """
    Configuración principal de la aplicación Flask.
    Todas las credenciales y claves sensibles deben definirse en el archivo .env.
    """
    # Clave secreta obligatoria para manejar sesiones y mensajes Flash (Notificaciones)
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-d1-default")

    # Credenciales exclusivas para la conexión con PostgreSQL mediante psycopg2
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "postgres")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_PORT = os.getenv("DB_PORT", "5432")