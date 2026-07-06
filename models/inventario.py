from extensions import db

class Inventario(db.Model):
    __tablename__ = 'Inventario'
    
    id_inventario = db.Column(db.Integer, primary_key=True)
    id_sede = db.Column(db.Integer, nullable=False) # Simplificado sin FK estricto para no generar toda la BD de Sedes
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad_disponible = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)
    stock_maximo = db.Column(db.Integer, default=0)
    
    producto = db.relationship('Producto', backref='inventarios')