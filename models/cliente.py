from extensions import db

class Cliente(db.Model):
    __tablename__ = 'Cliente'
    
    id_cliente = db.Column(db.Integer, primary_key=True)
    tipo_documento = db.Column(db.String(5), nullable=False)
    numero_documento = db.Column(db.String(20), nullable=False)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    telefono_cliente = db.Column(db.String(15))
    correo_cliente = db.Column(db.String(100), unique=True)
    habeas_data = db.Column(db.Boolean, nullable=False, default=False)