import math
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.empleado import EmpleadoModel
from models.sede import SedeModel

empleados_bp = Blueprint('empleados', __name__)

@empleados_bp.route('/')
def listar():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', None)
    orden_columna = request.args.get('orden_columna', 'id_empleado')
    orden_direccion = request.args.get('orden_direccion', 'ASC')
    
    per_page = 100
    offset = (page - 1) * per_page
    
    empleados = EmpleadoModel.obtener_paginados(per_page, offset, busqueda, orden_columna, orden_direccion)
    total_registros = EmpleadoModel.contar_total(busqueda)
    total_paginas = math.ceil(total_registros / per_page) if total_registros > 0 else 1
    
    return render_template(
        'empleados/listar.html', 
        empleados=empleados,
        page=page,
        total_paginas=total_paginas,
        busqueda=busqueda,
        orden_columna=orden_columna,
        orden_direccion=orden_direccion
    )

@empleados_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            EmpleadoModel.crear(datos)
            flash('Empleado registrado exitosamente.', 'success')
            return redirect(url_for('empleados.listar'))
        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash('Error general al registrar empleado. Verifica los datos.', 'danger')
            
    sedes = SedeModel.obtener_todas()
    return render_template('empleados/nuevo.html', sedes=sedes)

@empleados_bp.route('/editar/<int:id_empleado>', methods=['GET', 'POST'])
def editar(id_empleado):
    empleado = EmpleadoModel.obtener_por_id(id_empleado)
    if not empleado:
        flash('Empleado no encontrado.', 'warning')
        return redirect(url_for('empleados.listar'))

    if request.method == 'POST':
        try:
            datos = request.form.to_dict()
            EmpleadoModel.actualizar(id_empleado, datos)
            flash('Empleado actualizado exitosamente.', 'success')
            return redirect(url_for('empleados.listar'))
        except Exception as e:
            flash('Error al actualizar el empleado.', 'danger')

    sedes = SedeModel.obtener_todas()
    return render_template('empleados/editar.html', empleado=empleado, sedes=sedes)

@empleados_bp.route('/eliminar/<int:id_empleado>', methods=['POST'])
def eliminar(id_empleado):
    try:
        EmpleadoModel.eliminar(id_empleado)
        flash('Empleado eliminado exitosamente.', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    return redirect(url_for('empleados.listar'))