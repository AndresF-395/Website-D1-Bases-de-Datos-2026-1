import math
import uuid
from flask import jsonify
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.factura import FacturaModel
from models.detalle_factura import DetalleFacturaModel
from models.cliente import ClienteModel
from models.empleado import EmpleadoModel
from models.producto import ProductoModel

facturas_bp = Blueprint('facturas', __name__)

@facturas_bp.route('/')
def listar():
    page = request.args.get('page', 1, type=int)
    busqueda = request.args.get('busqueda', None)
    orden_columna = request.args.get('orden_columna', 'fecha_emision')
    orden_direccion = request.args.get('orden_direccion', 'DESC')
    
    per_page = 100
    offset = (page - 1) * per_page
    
    facturas = FacturaModel.obtener_paginados(per_page, offset, busqueda, orden_columna, orden_direccion)
    total_registros = FacturaModel.contar_total(busqueda)
    total_paginas = math.ceil(total_registros / per_page) if total_registros > 0 else 1
    
    return render_template(
        'facturas/listar.html', 
        facturas=facturas,
        page=page,
        total_paginas=total_paginas,
        busqueda=busqueda,
        orden_columna=orden_columna,
        orden_direccion=orden_direccion
    )


@facturas_bp.route('/nuevo', methods=['GET', 'POST'])
@facturas_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        # Captura de datos de cabecera enviados por el form
        id_cliente = request.form.get('id_cliente')
        id_empleado = request.form.get('id_empleado')
        id_sede = request.form.get('id_sede')
        forma_pago = request.form.get('forma_pago')
        
        # Solo confiamos en los IDs de productos y cantidades enviadas
        productos = request.form.getlist('productos[]')
        cantidades = request.form.getlist('cantidades[]')

        suma_subtotal = 0.0
        suma_iva = 0.0
        lista_detalles = []

        # Recálculo matemático estricto en el Backend para evitar valor = 0
        for i in range(len(productos)):
            if not productos[i]: 
                continue
                
            id_prod = int(productos[i])
            cant = int(cantidades[i])
            
            # Consultamos el precio y el IVA real desde la base de datos de forma segura
            prod_db = ProductoModel.obtener_por_id(id_prod)
            precio_real = float(prod_db['precio_venta'])
            tipo_iva = prod_db['tipo_iva']
            
            porcentaje_iva = 0.19 if tipo_iva == 'GENERAL' else (0.05 if tipo_iva == 'DIFERENCIAL' else 0.0)
            
            sub_linea = precio_real * cant
            iva_linea = sub_linea * porcentaje_iva
            
            detalle = {
                'id_producto': id_prod,
                'cantidad': cant,
                'precio_unitario_aplicado': precio_real,
                'subtotal_linea': sub_linea,
                'iva_aplicado': iva_linea
            }
            lista_detalles.append(detalle)
            
            suma_subtotal += sub_linea
            suma_iva += iva_linea

        total_facturado = suma_subtotal + suma_iva

        datos_factura = {
            'numero_factura_oficial': f"SETT-{uuid.uuid4().hex[:6].upper()}",
            'id_cliente': id_cliente,
            'id_sede': id_sede,
            'id_empleado': id_empleado,
            'forma_pago': forma_pago,
            'subtotal': suma_subtotal,
            'total_iva': suma_iva,
            'total_descuento': 0, 
            'total_factura': total_facturado,
            'valor_pagado': total_facturado, 
            'cambio_devuelto': 0
        }

        try:
            id_nueva_factura = FacturaModel.crear_con_detalles(datos_factura, lista_detalles)
            flash(f"Venta registrada con éxito. Total cobrado: ${total_facturado:,.2f}", 'success')
            return redirect(url_for('facturas.detalles', id_factura=id_nueva_factura))
        except Exception as e:
            flash(f"Error al registrar la venta: {str(e)}", 'danger')

    # Si es GET, cargamos datos segmentados para la vista
    sedes, clientes, empleados, inventario = FacturaModel.obtener_datos_pos()
    return render_template('facturas/nuevo.html', sedes=sedes, clientes=clientes, empleados=empleados, inventario=inventario)

# --- NUEVA RUTA PARA CREAR CLIENTES DESDE VENTAS ---
@facturas_bp.route('/api/cliente/rapido', methods=['POST'])
def crear_cliente_rapido():
    try:
        datos = request.json
        # Insertar en modelo (asegúrate de que tu ClienteModel tenga el método crear que reciba diccionario)
        id_cliente = ClienteModel.crear(datos)
        return jsonify({'success': True, 'id_cliente': id_cliente, 'nombre': f"{datos['nombres']} {datos['apellidos']}", 'doc': datos['numero_documento']})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
        
        
@facturas_bp.route('/detalles/<int:id_factura>')
def detalles(id_factura):
    """Muestra el detalle de una factura inmutable."""
    factura = FacturaModel.obtener_por_id(id_factura)
    if not factura:
        flash('Factura no encontrada.', 'warning')
        return redirect(url_for('facturas.listar'))
        
    detalles = DetalleFacturaModel.obtener_por_factura(id_factura)
    return render_template('facturas/detalles.html', factura=factura, detalles=detalles)

# NOTA: En la capa de vista de Creación (Fase 5) manejaremos los detalles mediante JavaScript 
# para enviar un arreglo JSON al controlador, o utilizando formularios dinámicos.