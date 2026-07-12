from flask import Flask, render_template

from config import Config

# ==============================================================================
# IMPORTACIÓN DE BLUEPRINTS (RUTAS)
# Estos módulos se generarán en la Fase 4 y gestionarán las peticiones HTTP.
# ==============================================================================
from routes.dashboard import dashboard_bp
from routes.clientes import clientes_bp
from routes.proveedores import proveedores_bp
from routes.productos import productos_bp
from routes.inventario import inventario_bp
from routes.facturas import facturas_bp
from routes.ordenes import ordenes_bp
from routes.empleados import empleados_bp
from routes.sedes import sedes_bp



def create_app():
    """
    Fábrica de la aplicación (Application Factory).
    Inicializa Flask, carga la configuración y registra los componentes.
    """
    app = Flask(__name__)
    @app.route('/')
    def index():
        return render_template('index.html')
    # Cargar la configuración desde config.py
    app.config.from_object(Config)

    # ==========================================================================
    # REGISTRO DE BLUEPRINTS (Descomentar en la Fase 4)
    # ==========================================================================
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    app.register_blueprint(proveedores_bp, url_prefix='/proveedores')
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(inventario_bp, url_prefix='/inventario')
    app.register_blueprint(facturas_bp, url_prefix='/facturas')
    app.register_blueprint(ordenes_bp, url_prefix='/ordenes')
    app.register_blueprint(empleados_bp, url_prefix='/empleados')
    app.register_blueprint(sedes_bp, url_prefix='/sedes')

    # ==========================================================================
    # MANEJO DE ERRORES GLOBALES
    # ==========================================================================
    @app.errorhandler(404)
    def page_not_found(error):
        """Maneja las rutas no encontradas y renderiza un template 404."""
        # Se asume la creación de un template base de error en la Fase 5
        # return render_template('errores/404.html'), 404
        return "Error 404: Página no encontrada", 404

    @app.errorhandler(500)
    def internal_server_error(error):
        """Maneja errores internos del servidor."""
        # return render_template('errores/500.html'), 500
        return "Error 500: Error interno del servidor", 500

    return app

# Punto de entrada de la aplicación
if __name__ == "__main__":
    app = create_app()
    # Debug activado solo para desarrollo. En producción debe ser False.
    app.run(host="0.0.0.0", port=5000, debug=True)