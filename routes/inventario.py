import math
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.inventario import InventarioModel
from models.producto import ProductoModel
from models.sede import SedeModel

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/')
def listar():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', None)
    orden_columna = request.args.get('orden_columna', 'id_inventario')
    orden_direccion = request.args.get('orden_direccion', 'ASC')
    
    per_page = 100
    offset = (page - 1) * per_page
    
    inventarios_raw = InventarioModel.obtener_paginados(per_page, offset, busqueda, orden_columna, orden_direccion)
    
    # Lógica de cálculo de Días de Stock y Categorización
    inventarios = []
    for inv in inventarios_raw:
        inv_dict = dict(inv)
        cantidad = inv_dict['cantidad_disponible']
        demanda = inv_dict.get('demanda_diaria', 0)
        
        # Evitar división por cero
        if cantidad == 0:
            dias_stock = 0
        elif demanda == 0:
            dias_stock = 999 # Valor alto si hay stock pero no hay demanda registrada
        else:
            dias_stock = cantidad / demanda

        # Categorización según las reglas de negocio
        if dias_stock == 0:
            inv_dict['estado'] = 'AGOTADO'
            inv_dict['accion'] = 'Pedido Inmediato'
            inv_dict['color'] = 'danger'
        elif dias_stock < 5:
            inv_dict['estado'] = 'CRÍTICO'
            inv_dict['accion'] = 'Pedido de Emergencia'
            inv_dict['color'] = 'warning'
        elif 5 <= dias_stock <= 15:
            inv_dict['estado'] = 'ALERTA'
            inv_dict['accion'] = 'Realizar Pedido Normal'
            inv_dict['color'] = 'info'
        else:
            inv_dict['estado'] = 'SEGURO'
            inv_dict['accion'] = 'Mantener Monitoreo'
            inv_dict['color'] = 'success'
            
        inv_dict['dias_stock_display'] = round(dias_stock, 1) if dias_stock != 999 else "∞"
        inventarios.append(inv_dict)

    total_registros = InventarioModel.contar_total(busqueda)
    total_paginas = math.ceil(total_registros / per_page) if total_registros > 0 else 1
    
    return render_template(
        'inventario/listar.html', 
        inventarios=inventarios,
        page=page,
        total_paginas=total_paginas,
        busqueda=busqueda,
        orden_columna=orden_columna,
        orden_direccion=orden_direccion
    )

@inventario_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            InventarioModel.crear(datos)
            flash('Inventario registrado exitosamente.', 'success')
            return redirect(url_for('inventario.listar'))
        except Exception as e:
            flash('Error al registrar inventario. Verifica que el producto no esté ya asignado a esa sede.', 'danger')
            
    # Cargar datos para los selectores (dropdowns)
    # limit=1000 temporal para selectores, idealmente esto se maneja con select2 y AJAX en el frontend
    productos = ProductoModel.obtener_paginados(limit=1000) 
    sedes = SedeModel.obtener_todas()
    
    return render_template('inventario/nuevo.html', productos=productos, sedes=sedes)

@inventario_bp.route('/editar/<int:id_inventario>', methods=['GET', 'POST'])
def editar(id_inventario):
    inventario = InventarioModel.obtener_por_id(id_inventario)
    if not inventario:
        flash('Registro de inventario no encontrado.', 'warning')
        return redirect(url_for('inventario.listar'))

    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            InventarioModel.actualizar(id_inventario, datos)
            flash('Inventario actualizado exitosamente.', 'success')
            return redirect(url_for('inventario.listar'))
        except Exception as e:
            flash('Error al actualizar el inventario.', 'danger')

    productos = ProductoModel.obtener_paginados(limit=1000)
    sedes = SedeModel.obtener_todas()
    return render_template('inventario/editar.html', inventario=inventario, productos=productos, sedes=sedes)

@inventario_bp.route('/eliminar/<int:id_inventario>', methods=['POST'])
def eliminar(id_inventario):
    try:
        InventarioModel.eliminar(id_inventario)
        flash('Registro de inventario eliminado exitosamente.', 'success')
    except Exception as e:
        flash('Error al eliminar el inventario.', 'danger')
    return redirect(url_for('inventario.listar'))