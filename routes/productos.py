import math
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.producto import ProductoModel
from models.proveedor import ProveedorModel

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/')
def listar():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', None)
    orden_columna = request.args.get('orden_columna', 'nombre_producto')
    orden_direccion = request.args.get('orden_direccion', 'ASC')
    
    per_page = 100
    offset = (page - 1) * per_page
    
    productos = ProductoModel.obtener_paginados(per_page, offset, busqueda, orden_columna, orden_direccion)
    total_registros = ProductoModel.contar_total(busqueda)
    total_paginas = math.ceil(total_registros / per_page) if total_registros > 0 else 1
    
    return render_template(
        'productos/listar.html', 
        productos=productos,
        page=page,
        total_paginas=total_paginas,
        busqueda=busqueda,
        orden_columna=orden_columna,
        orden_direccion=orden_direccion
    )

@productos_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            datos['fecha_vencimiento'] = datos.get('fecha_vencimiento') or None
            ProductoModel.crear(datos)
            flash('Producto registrado exitosamente.', 'success')
            return redirect(url_for('productos.listar'))
        except Exception as e:
            flash('Error al registrar producto. Código de barras duplicado o datos inválidos.', 'danger')
            
    proveedores = ProveedorModel.obtener_paginados(limit=1000)
    return render_template('productos/nuevo.html', proveedores=proveedores)

@productos_bp.route('/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar(id_producto):
    producto = ProductoModel.obtener_por_id(id_producto)
    if not producto:
        flash('Producto no encontrado o inactivo.', 'warning')
        return redirect(url_for('productos.listar'))

    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            datos['fecha_vencimiento'] = datos.get('fecha_vencimiento') or None
            ProductoModel.actualizar(id_producto, datos)
            flash('Producto actualizado exitosamente.', 'success')
            return redirect(url_for('productos.listar'))
        except Exception as e:
            flash('Error al actualizar el producto.', 'danger')

    proveedores = ProveedorModel.obtener_paginados(limit=1000)
    return render_template('productos/editar.html', producto=producto, proveedores=proveedores)

@productos_bp.route('/eliminar/<int:id_producto>', methods=['POST'])
def eliminar(id_producto):
    try:
        # Se ejecuta eliminación lógica, no física
        ProductoModel.eliminar_logico(id_producto)
        flash('Producto desactivado exitosamente (Eliminación lógica).', 'success')
    except Exception as e:
        flash('Error al desactivar el producto.', 'danger')
    return redirect(url_for('productos.listar'))
