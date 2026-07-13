import math
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.sede import SedeModel
from models.empleado import EmpleadoModel # Importamos el modelo de empleados

sedes_bp = Blueprint('sedes', __name__)

@sedes_bp.route('/')
def listar():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', None)
    orden_columna = request.args.get('orden_columna', 'nombre_sede')
    orden_direccion = request.args.get('orden_direccion', 'ASC')
    
    per_page = 100
    offset = (page - 1) * per_page
    
    sedes = SedeModel.obtener_paginados(per_page, offset, busqueda, orden_columna, orden_direccion)
    total_paginas = 1
    
    return render_template(
        'sedes/listar.html', 
        sedes=sedes,
        page=page,
        total_paginas=total_paginas,
        busqueda=busqueda,
        orden_columna=orden_columna,
        orden_direccion=orden_direccion
    )

@sedes_bp.route('/detalles/<int:id_sede>')
def detalles(id_sede):
    """Muestra la ficha técnica de la sede junto con su personal asignado."""
    sede = SedeModel.obtener_por_id(id_sede)
    if not sede:
        flash('Sede no encontrada.', 'warning')
        return redirect(url_for('sedes.listar'))
    
    # Buscamos los empleados que corresponden a esta sede
    personal = EmpleadoModel.obtener_por_sede(id_sede)
    return render_template('sedes/detalles.html', sede=sede, personal=personal)