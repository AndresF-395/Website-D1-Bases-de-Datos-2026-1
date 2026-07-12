import math
import uuid
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
def nuevo():
    if request.method == 'POST':
        # Captura de datos de cabecera
        id_cliente = request.form.get('id_cliente')
        id_empleado = request.form.get('id_empleado')
        forma_pago = request.form.get('forma_pago')
        
        # Para este ejemplo, asignamos la sede 1 por defecto, o puedes traerla del empleado seleccionado
        id_sede = 1 
        
        # Captura de arrays (detalles)
        productos = request.form.getlist('productos[]')
        precios = request.form.getlist('precios[]')
        cantidades = request.form.getlist('cantidades[]')
        subtotales = request.form.getlist('subtotales[]')
        ivas = request.form.getlist('ivas[]')

        # Variables para sumarizador
        suma_subtotal = 0.0
        suma_iva = 0.0
        lista_detalles = []

        # Procesar cada línea de la factura
        for i in range(len(productos)):
            if not productos[i]: # Prevenir líneas vacías
                continue
                
            sub_linea = float(subtotales[i])
            iva_linea = float(ivas[i])
            
            detalle = {
                'id_producto': int(productos[i]),
                'cantidad': int(cantidades[i]),
                'precio_unitario_aplicado': float(precios[i]),
                'subtotal_linea': sub_linea,
                'iva_aplicado': iva_linea
            }
            lista_detalles.append(detalle)
            
            suma_subtotal += sub_linea
            suma_iva += iva_linea

        total_facturado = suma_subtotal + suma_iva

        # Empaquetar la cabecera
        datos_factura = {
            # Generar un prefijo DIAN y un identificador único para el proyecto
            'numero_factura_oficial': f"SETT-{uuid.uuid4().hex[:6].upper()}",
            'id_cliente': id_cliente,
            'id_sede': id_sede,
            'id_empleado': id_empleado,
            'forma_pago': forma_pago,
            'subtotal': suma_subtotal,
            'total_iva': suma_iva,
            'total_descuento': 0, # Según reglas, 0 por defecto
            'total_factura': total_facturado,
            'valor_pagado': total_facturado, # Asumimos pago exacto
            'cambio_devuelto': 0
        }

        try:
            id_nueva_factura = FacturaModel.crear_con_detalles(datos_factura, lista_detalles)
            flash(f"Venta registrada con éxito. IVA calculado: ${suma_iva:,.2f}", 'success')
            return redirect(url_for('facturas.detalles', id_factura=id_nueva_factura))
        except Exception as e:
            flash(f"Error al registrar la venta: {str(e)}", 'danger')

    # Si es GET, cargamos datos para los selects
    clientes = ClienteModel.obtener_paginados(limit=1000)
    empleados = EmpleadoModel.obtener_paginados(limit=100)
    productos = ProductoModel.obtener_paginados(limit=1000)
    
    return render_template('facturas/nuevo.html', clientes=clientes, empleados=empleados, productos=productos)
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