from flask import Flask, render_template
from config import Config
from extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Registro de rutas (Blueprints)
    from routes import clientes, proveedores, inventario, facturas, ordenes
    app.register_blueprint(clientes.bp)
    app.register_blueprint(proveedores.bp)
    app.register_blueprint(inventario.bp)
    app.register_blueprint(facturas.bp)
    app.register_blueprint(ordenes.bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)