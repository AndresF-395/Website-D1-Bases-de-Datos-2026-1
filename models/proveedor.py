from extensions import db

class Proveedor(db.Model):
    __tablename__ = 'Proveedor'
    
    nit_proveedor = db.Column(db.String(20), primary_key=True)
    nombre_proveedor = db.Column(db.String(100), nullable=False)
    direccion_empresa = db.Column(db.String(150), nullable=False)
    telefono_proveedor = db.Column(db.String(15))
    correo_proveedor = db.Column(db.String(100), unique=True)