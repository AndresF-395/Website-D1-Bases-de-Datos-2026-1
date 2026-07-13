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
            # Convertimos el formulario en un diccionario mutable
            datos = request.form.to_dict()
            
            # 1. Saneamiento de campos opcionales y fechas
            datos['fecha_vencimiento'] = datos.get('fecha_vencimiento') or None
            
            # 2. Casteo explícito a tipos numéricos requeridos por la BD
            datos['precio_compra'] = float(datos['precio_compra']) if datos.get('precio_compra') else 0.0
            datos['precio_venta'] = float(datos['precio_venta']) if datos.get('precio_venta') else 0.0
            
            if not datos.get('demanda_diaria') or datos['demanda_diaria'].strip() == "":
                datos['demanda_diaria'] = 0
            else:
                datos['demanda_diaria'] = int(datos['demanda_diaria'])
            
            # 3. Intentar la creación en el modelo
            ProductoModel.crear(datos)
            flash('Producto registrado exitosamente.', 'success')
            return redirect(url_for('productos.listar'))
            
        except Exception as e:
            # DEPURACIÓN: Esto expondrá la verdadera razón en la consola de comandos
            print("=========================================")
            print(f"ERROR REAL EN CREACIÓN: {str(e)}")
            print("=========================================")
            
            # Le mostramos el error detallado en la interfaz web
            flash(f'Error al registrar producto: {str(e)}', 'danger')
            
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
            # Convertimos el ImmutableMultiDict de Flask a un diccionario mutable
            datos = request.form.to_dict()
            
            # 1. Saneamiento de fechas (evitar cadenas vacías)
            datos['fecha_vencimiento'] = datos.get('fecha_vencimiento') or None
            
            # 2. Casteo explícito a tipos numéricos para evitar que se vayan como texto ("")
            datos['precio_compra'] = float(datos['precio_compra']) if datos.get('precio_compra') else 0.0
            datos['precio_venta'] = float(datos['precio_venta']) if datos.get('precio_venta') else 0.0
            
            # Si demanda_diaria viene vacío "", lo convertimos formalmente en 0 numérico
            if not datos.get('demanda_diaria') or datos['demanda_diaria'].strip() == "":
                datos['demanda_diaria'] = 0
            else:
                datos['demanda_diaria'] = int(datos['demanda_diaria'])

            # 3. Ejecutar la actualización en el modelo
            ProductoModel.actualizar(id_producto, datos)
            flash('Producto actualizado exitosamente.', 'success')
            return redirect(url_for('productos.listar'))
            
        except Exception as e:
            # DEPURACIÓN: Esto imprimirá el error real (ej: Violación de CHECK, etc.) en tu terminal de ejecución
            print("=========================================")
            print(f"ERROR REAL EN POSTGRESQL/PYTHON: {str(e)}")
            print("=========================================")
            
            # Le mostramos el error detallado en la alerta de Flask para que sepas qué falló
            flash(f'Error al actualizar el producto: {str(e)}', 'danger')

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
