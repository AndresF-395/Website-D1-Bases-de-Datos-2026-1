import math
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.proveedor import ProveedorModel

proveedores_bp = Blueprint('proveedores', __name__)

@proveedores_bp.route('/')
def listar():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', None)
    orden_columna = request.args.get('orden_columna', 'nombre_proveedor')
    orden_direccion = request.args.get('orden_direccion', 'ASC')
    
    per_page = 100
    offset = (page - 1) * per_page
    
    proveedores = ProveedorModel.obtener_paginados(per_page, offset, busqueda, orden_columna, orden_direccion)
    total_registros = ProveedorModel.contar_total(busqueda)
    total_paginas = math.ceil(total_registros / per_page) if total_registros > 0 else 1
    
    return render_template(
        'proveedores/listar.html', 
        proveedores=proveedores,
        page=page,
        total_paginas=total_paginas,
        busqueda=busqueda,
        orden_columna=orden_columna,
        orden_direccion=orden_direccion
    )

@proveedores_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            ProveedorModel.crear(datos)
            flash('Proveedor registrado exitosamente.', 'success')
            return redirect(url_for('proveedores.listar'))
        except Exception as e:
            flash('Error al registrar proveedor. Verifica que el NIT o correo no estén duplicados.', 'danger')
            
    return render_template('proveedores/nuevo.html')

@proveedores_bp.route('/editar/<string:nit_proveedor>', methods=['GET', 'POST'])
def editar(nit_proveedor):
    proveedor = ProveedorModel.obtener_por_nit(nit_proveedor)
    if not proveedor:
        flash('Proveedor no encontrado.', 'warning')
        return redirect(url_for('proveedores.listar'))

    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            ProveedorModel.actualizar(nit_proveedor, datos)
            flash('Proveedor actualizado exitosamente.', 'success')
            return redirect(url_for('proveedores.listar'))
        except Exception as e:
            flash('Error al actualizar proveedor.', 'danger')

    return render_template('proveedores/editar.html', proveedor=proveedor)

@proveedores_bp.route('/eliminar/<string:nit_proveedor>', methods=['POST'])
def eliminar(nit_proveedor):
    try:
        ProveedorModel.eliminar(nit_proveedor)
        flash('Proveedor eliminado exitosamente.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('proveedores.listar'))