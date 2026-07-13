import math
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.orden import OrdenModel
from models.detalle_pedido import DetallePedidoModel
from models.proveedor import ProveedorModel
from models.empleado import EmpleadoModel
from models.producto import ProductoModel
from psycopg2.extras import RealDictCursor
from conexion import conectar

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
        conexion = conectar() # Abrimos conexión manual para validar precios seguros
        try:
            id_sede = request.form.get('id_sede')
            nit_proveedor = request.form.get('nit_proveedor')
            id_empleado = request.form.get('id_empleado')
            fecha_orden = request.form.get('fecha_orden') or None
            lugar_entrega = request.form.get('lugar_entrega')

            productos = request.form.getlist('productos[]')
            cantidades = request.form.getlist('cantidades[]')

            lista_detalles = []
            total = 0.0

            with conexion.cursor(cursor_factory=RealDictCursor) as cursor:
                # Recálculo matemático en el backend usando la tabla Productos_Por_Proveedor
                for i, id_producto in enumerate(productos):
                    if not id_producto:
                        continue

                    cantidad = int(float(cantidades[i]))
                    if cantidad < 1:
                        raise ValueError('La cantidad mínima por producto es 1.')

                    # Buscamos el precio real de compra negociado con ESTE proveedor
                    cursor.execute("""
                        SELECT precio_compra 
                        FROM Productos_Por_Proveedor 
                        WHERE codigo_producto = %s AND nit_proveedor = %s AND activo = TRUE
                    """, (int(id_producto), nit_proveedor))
                    
                    producto_proveedor = cursor.fetchone()
                    if not producto_proveedor:
                         raise ValueError(f'El producto {id_producto} no está vinculado activamente a este proveedor.')

                    costo = float(producto_proveedor['precio_compra'])
                    subtotal = cantidad * costo
                    
                    lista_detalles.append({
                        'id_producto': int(id_producto),
                        'cantidad': cantidad,
                        'precio_compra_unitario': costo,
                        'subtotal_pedido': subtotal
                    })
                    total += subtotal

            if not lista_detalles:
                raise ValueError('Debe agregar al menos un producto a la orden.')

            datos_orden = {
                'nit_proveedor': nit_proveedor,
                'id_sede': id_sede,
                'fecha_pedido': fecha_orden,
                'estado_pedido': 'PENDIENTE',
                'total': total,
                'lugar_entrega': lugar_entrega
            }

            id_orden = OrdenModel.crear_con_detalles(datos_orden, lista_detalles)
            flash('Orden de pedido registrada exitosamente.', 'success')
            return redirect(url_for('ordenes.detalles', id_orden_pedido=id_orden))
        
        except Exception as e:
            flash(f'Error al registrar la orden: {str(e)}', 'danger')
        finally:
            conexion.close()

    # Si es GET, cargamos los datos
    sedes, proveedores, empleados, productos = OrdenModel.obtener_datos_pedido()

    return render_template('ordenes/nuevo.html', 
                           sedes=sedes, 
                           proveedores=proveedores, 
                           empleados=empleados, 
                           productos=productos)

@ordenes_bp.route('/detalles/<int:id_orden_pedido>')
def detalles(id_orden_pedido):
    orden = OrdenModel.obtener_por_id(id_orden_pedido)
    if not orden:
        flash('Orden no encontrada.', 'warning')
        return redirect(url_for('ordenes.listar'))

    detalles_orden = DetallePedidoModel.obtener_por_orden(id_orden_pedido)
    return render_template('ordenes/detalles.html', orden=orden, detalles=detalles_orden)
