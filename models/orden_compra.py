from extensions import db
from datetime import datetime

class OrdenPedido(db.Model):
    __tablename__ = 'Ordenes_Pedidos'
    
    id_orden_pedido = db.Column(db.Integer, primary_key=True)
    nit_proveedor = db.Column(db.String(20), db.ForeignKey('proveedor.nit_proveedor'), nullable=False)
    id_sede = db.Column(db.Integer, nullable=False)
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    estado_pedido = db.Column(db.String(20), default='PENDIENTE')
    total = db.Column(db.Numeric(12,2), default=0)

    proveedor = db.relationship('Proveedor', backref='ordenes')