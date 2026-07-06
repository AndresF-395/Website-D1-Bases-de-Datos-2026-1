from extensions import db

class Producto(db.Model):
    __tablename__ = 'Productos'
    
    id_producto = db.Column(db.Integer, primary_key=True)
    codigo_de_barras = db.Column(db.String(30), unique=True, nullable=False)
    nombre_producto = db.Column(db.String(80), nullable=False)
    tipo_de_producto = db.Column(db.String(50), nullable=False)
    precio_compra = db.Column(db.Numeric(12,2), nullable=False)
    precio_venta = db.Column(db.Numeric(12,2), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    fecha_vencimiento = db.Column(db.Date)
    tipo_iva = db.Column(db.String(15), default='EXCLUIDO')
    activo = db.Column(db.Boolean, default=True)