from flask import Blueprint, render_template, request
from models.inventario import Inventario
from models.producto import Producto
from services.inventario_service import InventarioService

bp = Blueprint('inventario', __name__, url_prefix='/inventario')

@bp.route('/')
def index():
    inventarios = Inventario.query.join(Producto).filter(Producto.activo == True).all()
    
    # Se simula una demanda diaria de 10 unidades ya que el SQL no la contempla
    DEMANDA_SIMULADA = 10 
    
    datos = []
    for inv in inventarios:
        estado = InventarioService.calcular_estado_stock(inv.cantidad_disponible, DEMANDA_SIMULADA)
        datos.append({'inv': inv, 'estado': estado, 'demanda': DEMANDA_SIMULADA})
        
    return render_template('inventario/index.html', datos=datos)