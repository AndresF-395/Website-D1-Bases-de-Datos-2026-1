import math
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.cliente import ClienteModel

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/')
def listar():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', None)
    orden_columna = request.args.get('orden_columna', 'id_cliente')
    orden_direccion = request.args.get('orden_direccion', 'ASC')
    
    per_page = 100
    offset = (page - 1) * per_page
    
    clientes = ClienteModel.obtener_paginados(per_page, offset, busqueda, orden_columna, orden_direccion)
    total_registros = ClienteModel.contar_total(busqueda)
    total_paginas = math.ceil(total_registros / per_page) if total_registros > 0 else 1
    
    return render_template(
        'clientes/listar.html', 
        clientes=clientes,
        page=page,
        total_paginas=total_paginas,
        busqueda=busqueda,
        orden_columna=orden_columna,
        orden_direccion=orden_direccion
    )

@clientes_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        try:
            datos = {
                'tipo_documento': request.form['tipo_documento'],
                'numero_documento': request.form['numero_documento'],
                'nombres': request.form['nombres'],
                'apellidos': request.form['apellidos'],
                'telefono_cliente': request.form.get('telefono_cliente'),
                'correo_cliente': request.form.get('correo_cliente'),
                'direccion_residencia': request.form.get('direccion_residencia'),
                'habeas_data': True if request.form.get('habeas_data') else False
            }
            ClienteModel.crear(datos)
            flash('Cliente registrado exitosamente.', 'success')
            return redirect(url_for('clientes.listar'))
        except Exception as e:
            flash(f'Error al registrar cliente: Verifica que el documento o correo no estén duplicados.', 'danger')
            
    return render_template('clientes/nuevo.html')

@clientes_bp.route('/editar/<int:id_cliente>', methods=['GET', 'POST'])
def editar(id_cliente):
    cliente = ClienteModel.obtener_por_id(id_cliente)
    if not cliente:
        flash('Cliente no encontrado.', 'warning')
        return redirect(url_for('clientes.listar'))

    if request.method == 'POST':
        try:
            datos = {
                'nombres': request.form['nombres'],
                'apellidos': request.form['apellidos'],
                'telefono_cliente': request.form.get('telefono_cliente'),
                'correo_cliente': request.form.get('correo_cliente'),
                'direccion_residencia': request.form.get('direccion_residencia'),
                'habeas_data': True if request.form.get('habeas_data') else False
            }
            # NOTA: No capturamos documento ni tipo_documento para proteger la integridad histórica
            ClienteModel.actualizar(id_cliente, datos)
            flash('Datos del cliente actualizados exitosamente.', 'success')
            return redirect(url_for('clientes.listar'))
        except Exception as e:
            flash(f'Error al actualizar el cliente. Verifica la información.', 'danger')

    return render_template('clientes/editar.html', cliente=cliente)

@clientes_bp.route('/eliminar/<int:id_cliente>', methods=['POST'])
def eliminar(id_cliente):
    try:
        ClienteModel.eliminar(id_cliente)
        flash('Cliente eliminado exitosamente.', 'success')
    except ValueError as e:
        # Capturamos el error de Integridad Referencial emitido por el Modelo
        flash(str(e), 'danger')
    return redirect(url_for('clientes.listar'))