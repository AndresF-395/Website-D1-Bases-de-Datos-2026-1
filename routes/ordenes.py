import math
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.orden import OrdenModel
from models.detalle_pedido import DetallePedidoModel

# Importaciones para el formulario nuevo
from models.proveedor import ProveedorModel
from models.empleado import EmpleadoModel
from models.producto import ProductoModel

ordenes_bp = Blueprint('ordenes', __name__)

@ordenes_bp.route('/')
def listar():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', None)
    orden_columna = request.args.get('orden_columna', 'fecha_pedido')
    orden_direccion = request.args.get('orden_direccion', 'DESC')
    
    per_page = 100
    offset = (page - 1) * per_page
    
    ordenes = OrdenModel.obtener_paginados(per_page, offset, busqueda, orden_columna, orden_direccion)
    total_registros = OrdenModel.contar_total(busqueda)
    total_paginas = math.ceil(total_registros / per_page) if total_registros > 0 else 1
    
    return render_template(
        'ordenes/listar.html', 
        ordenes=ordenes,
        page=page,
        total_paginas=total_paginas,
        busqueda=busqueda,
        orden_columna=orden_columna,
        orden_direccion=orden_direccion
    )

@ordenes_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        # La lógica de guardar la manejaremos después
        pass
        
    proveedores = ProveedorModel.obtener_paginados(limit=1000) if hasattr(ProveedorModel, 'obtener_paginados') else []
    empleados = EmpleadoModel.obtener_paginados(limit=100) if hasattr(EmpleadoModel, 'obtener_paginados') else []
    productos = ProductoModel.obtener_paginados(limit=1000) if hasattr(ProductoModel, 'obtener_paginados') else []
    
    return render_template('ordenes/nuevo.html', proveedores=proveedores, empleados=empleados, productos=productos)

@ordenes_bp.route('/detalles/<int:id_orden_pedido>')
def detalles(id_orden_pedido):
    """Muestra los artículos incluidos en una orden."""
    orden = OrdenModel.obtener_por_id(id_orden_pedido)
    if not orden:
        flash('Orden no encontrada.', 'warning')
        return redirect(url_for('ordenes.listar'))
        
    detalles_orden = DetallePedidoModel.obtener_por_orden(id_orden_pedido)
    return render_template('ordenes/detalles.html', orden=orden, detalles=detalles_orden)