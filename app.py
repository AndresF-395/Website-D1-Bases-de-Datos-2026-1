from flask import Flask, render_template, request, redirect
from conexion import conectar

app = Flask(__name__)


# Página principal
@app.route("/")
def inicio():
    return render_template("index.html")


# Página de productos
@app.route("/productos")
def productos():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_producto, codigo_de_barras, nombre_producto, 
               tipo_de_producto, precio_venta, marca
        FROM productos
        LIMIT 20;
    """)

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("productos.html", productos=productos)
@app.route("/clientes")
def clientes():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT id_cliente, tipo_documento, numero_documento,
           nombres, apellidos, telefono_cliente,
           correo_cliente, habeas_data
    FROM cliente
    ORDER BY id_cliente;
""")

    clientes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("clientes.html", clientes=clientes)
@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    if request.method == "POST":

        tipo_documento = request.form["tipo_documento"]
        numero_documento = request.form["numero_documento"]
        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        telefono = request.form["telefono_cliente"]
        correo = request.form["correo_cliente"]
        habeas = request.form["habeas_data"]

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO cliente
            (tipo_documento, numero_documento, nombres, apellidos,
             telefono_cliente, correo_cliente, habeas_data)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            tipo_documento,
            numero_documento,
            nombres,
            apellidos,
            telefono,
            correo,
            habeas
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/clientes")


    return render_template("nuevo_cliente.html")
@app.route("/clientes/editar/<int:id_cliente>", methods=["GET", "POST"])
def editar_cliente(id_cliente):

    conexion = conectar()
    cursor = conexion.cursor()

    if request.method == "POST":

        nombres = request.form["nombres"]
        apellidos = request.form["apellidos"]
        telefono = request.form["telefono_cliente"]
        correo = request.form["correo_cliente"]
        habeas = request.form["habeas_data"]

        cursor.execute("""
            UPDATE cliente
            SET nombres = %s,
                apellidos = %s,
                telefono_cliente = %s,
                correo_cliente = %s,
                habeas_data = %s
            WHERE id_cliente = %s
        """,
        (
            nombres,
            apellidos,
            telefono,
            correo,
            habeas,
            id_cliente
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/clientes")


    cursor.execute("""
        SELECT id_cliente, tipo_documento, numero_documento,
               nombres, apellidos, telefono_cliente,
               correo_cliente, habeas_data
        FROM cliente
        WHERE id_cliente = %s
    """, (id_cliente,))

    cliente = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template("editar_cliente.html", cliente=cliente)



@app.route("/clientes/eliminar/<int:id_cliente>")
def eliminar_cliente(id_cliente):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM cliente
        WHERE id_cliente = %s
    """, (id_cliente,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect("/clientes")
@app.route("/proveedores")
def proveedores():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT nit_proveedor, nombre_proveedor,
               direccion_empresa, telefono_proveedor,
               correo_proveedor
        FROM proveedor
        ORDER BY nombre_proveedor;
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template("proveedores.html", proveedores=proveedores)
@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():

    if request.method == "POST":

        nit = request.form["nit_proveedor"]
        nombre = request.form["nombre_proveedor"]
        direccion = request.form["direccion_empresa"]
        telefono = request.form["telefono_proveedor"]
        correo = request.form["correo_proveedor"]

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO proveedor
            (nit_proveedor, nombre_proveedor,
             direccion_empresa, telefono_proveedor,
             correo_proveedor)
            VALUES (%s,%s,%s,%s,%s)
        """,
        (
            nit,
            nombre,
            direccion,
            telefono,
            correo
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/proveedores")


    return render_template("nuevo_proveedor.html")
@app.route("/proveedores/editar/<string:nit_proveedor>", methods=["GET", "POST"])
def editar_proveedor(nit_proveedor):

    conexion = conectar()
    cursor = conexion.cursor()

    if request.method == "POST":

        nombre = request.form["nombre_proveedor"]
        direccion = request.form["direccion_empresa"]
        telefono = request.form["telefono_proveedor"]
        correo = request.form["correo_proveedor"]

        cursor.execute("""
            UPDATE proveedor
            SET nombre_proveedor = %s,
                direccion_empresa = %s,
                telefono_proveedor = %s,
                correo_proveedor = %s
            WHERE nit_proveedor = %s
        """,
        (
            nombre,
            direccion,
            telefono,
            correo,
            nit_proveedor
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/proveedores")


    cursor.execute("""
        SELECT nit_proveedor,
               nombre_proveedor,
               direccion_empresa,
               telefono_proveedor,
               correo_proveedor
        FROM proveedor
        WHERE nit_proveedor = %s
    """, (nit_proveedor,))

    proveedor = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template("editar_proveedor.html", proveedor=proveedor)
@app.route("/proveedores/eliminar/<string:nit_proveedor>")
def eliminar_proveedor(nit_proveedor):

    conexion = conectar()
    cursor = conexion.cursor()

    try:

        cursor.execute("""
            DELETE FROM proveedor
            WHERE nit_proveedor = %s
        """, (nit_proveedor,))

        conexion.commit()

    except Exception as e:

        conexion.rollback()

        cursor.close()
        conexion.close()

        return "No se puede eliminar este proveedor porque tiene registros asociados."


    cursor.close()
    conexion.close()

    return redirect("/proveedores")
# ==========================
# INVENTARIO
# ==========================

@app.route("/inventario")
def inventario():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            i.id_inventario,
            p.nombre_producto,
            s.nombre_sede,
            i.cantidad_disponible,
            i.stock_minimo,
            i.stock_maximo
        FROM inventario i
        INNER JOIN productos p
            ON i.id_producto = p.id_producto
        INNER JOIN sedes s
            ON i.id_sede = s.id_sede
        ORDER BY i.id_inventario;
    """)

    inventarios = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "inventario.html",
        inventarios=inventarios
    )


@app.route("/inventario/nuevo", methods=["GET", "POST"])
def nuevo_inventario():

    conexion = conectar()
    cursor = conexion.cursor()

    if request.method == "POST":

        id_producto = request.form["id_producto"]
        id_sede = request.form["id_sede"]
        cantidad = request.form["cantidad_disponible"]
        minimo = request.form["stock_minimo"]
        maximo = request.form["stock_maximo"]

        # Verificar si ya existe ese producto en esa sede
        cursor.execute("""
            SELECT *
            FROM inventario
            WHERE id_producto = %s
            AND id_sede = %s
        """, (id_producto, id_sede))

        existe = cursor.fetchone()

        if existe:

            cursor.execute("""
                SELECT id_producto, nombre_producto
                FROM productos
                ORDER BY nombre_producto
            """)
            productos = cursor.fetchall()

            cursor.execute("""
                SELECT id_sede, nombre_sede
                FROM sedes
                ORDER BY nombre_sede
            """)
            sedes = cursor.fetchall()

            cursor.close()
            conexion.close()

            return render_template(
                "nuevo_inventario.html",
                productos=productos,
                sedes=sedes,
                mensaje="Ese producto ya tiene inventario registrado en esa sede."
            )

        cursor.execute("""
            INSERT INTO inventario
            (
                id_producto,
                id_sede,
                cantidad_disponible,
                stock_minimo,
                stock_maximo
            )
            VALUES (%s,%s,%s,%s,%s)
        """,
        (
            id_producto,
            id_sede,
            cantidad,
            minimo,
            maximo
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/inventario")


    cursor.execute("""
        SELECT id_producto, nombre_producto
        FROM productos
        ORDER BY nombre_producto
    """)

    productos = cursor.fetchall()

    cursor.execute("""
        SELECT id_sede, nombre_sede
        FROM sedes
        ORDER BY nombre_sede
    """)

    sedes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "nuevo_inventario.html",
        productos=productos,
        sedes=sedes
    )


@app.route("/inventario/editar/<int:id>", methods=["GET", "POST"])
def editar_inventario(id):

    conexion = conectar()
    cursor = conexion.cursor()

    if request.method == "POST":

        id_producto = request.form["id_producto"]
        id_sede = request.form["id_sede"]
        cantidad = request.form["cantidad_disponible"]
        minimo = request.form["stock_minimo"]
        maximo = request.form["stock_maximo"]

        cursor.execute("""
            UPDATE inventario
            SET
                id_producto = %s,
                id_sede = %s,
                cantidad_disponible = %s,
                stock_minimo = %s,
                stock_maximo = %s
            WHERE id_inventario = %s
        """,
        (
            id_producto,
            id_sede,
            cantidad,
            minimo,
            maximo,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/inventario")


    cursor.execute("""
        SELECT
            id_inventario,
            id_producto,
            id_sede,
            cantidad_disponible,
            stock_minimo,
            stock_maximo
        FROM inventario
        WHERE id_inventario = %s
    """, (id,))

    inventario = cursor.fetchone()


    cursor.execute("""
        SELECT
            id_producto,
            nombre_producto
        FROM productos
        ORDER BY nombre_producto
    """)

    productos = cursor.fetchall()


    cursor.execute("""
        SELECT
            id_sede,
            nombre_sede
        FROM sedes
        ORDER BY nombre_sede
    """)

    sedes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "editar_inventario.html",
        inventario=inventario,
        productos=productos,
        sedes=sedes
    )

@app.route("/inventario/eliminar/<int:id>")
def eliminar_inventario(id):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM inventario
        WHERE id_inventario=%s
    """,(id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect("/inventario")
# ==========================
# FACTURAS
# ==========================

@app.route("/facturas")
def facturas():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            f.numero_factura_oficial,
            c.nombres || ' ' || c.apellidos AS cliente,
            s.nombre_sede,
            e.nombre_empleado,
            f.fecha_emision,
            f.forma_pago,
            f.total_factura,
            f.id_factura
        FROM factura f
        INNER JOIN cliente c
            ON f.id_cliente = c.id_cliente
        INNER JOIN sedes s
            ON f.id_sede = s.id_sede
        INNER JOIN empleados e
            ON f.id_empleado = e.id_empleado
        ORDER BY f.id_factura;
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "facturas.html",
        facturas=facturas
    )


@app.route("/facturas/nuevo", methods=["GET","POST"])
def nueva_factura():

    conexion = conectar()
    cursor = conexion.cursor()

    if request.method == "POST":

        numero = request.form["numero_factura_oficial"]
        cliente = request.form["id_cliente"]
        sede = request.form["id_sede"]
        empleado = request.form["id_empleado"]
        forma = request.form["forma_pago"]
        subtotal = float(request.form["subtotal"])
        iva = float(request.form["total_iva"])
        descuento = float(request.form["total_descuento"])
        total = float(request.form["total_factura"])
        pagado = float(request.form["valor_pagado"])

        cambio = round(pagado - total, 2)

        if cambio < 0:
            cambio = 0

        cursor.execute("""
    INSERT INTO factura
    (
        numero_factura_oficial,
        id_cliente,
        id_sede,
        id_empleado,
        fecha_emision,
        forma_pago,
        subtotal,
        total_iva,
        total_descuento,
        total_factura,
        valor_pagado,
        cambio_devuelto
    )
    VALUES
    (
        %s,%s,%s,%s,
        NOW(),
        %s,%s,%s,%s,%s,%s,%s
    )
""",
(
    numero,
    cliente,
    sede,
    empleado,
    forma,
    subtotal,
    iva,
    descuento,
    total,
    pagado,
    cambio
))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/facturas")

    cursor.execute("""
        SELECT
            id_cliente,
            nombres,
            apellidos
        FROM cliente
        ORDER BY nombres
    """)
    clientes = cursor.fetchall()

    cursor.execute("""
        SELECT
            id_sede,
            nombre_sede
        FROM sedes
        ORDER BY nombre_sede
    """)
    sedes = cursor.fetchall()

    cursor.execute("""
        SELECT
            id_empleado,
            nombre_empleado
        FROM empleados
        ORDER BY nombre_empleado
    """)
    empleados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "nuevo_factura.html",
        clientes=clientes,
        sedes=sedes,
        empleados=empleados
    )
@app.route("/facturas/editar/<int:id>", methods=["GET", "POST"])
def editar_factura(id):

    conexion = conectar()
    cursor = conexion.cursor()

    if request.method == "POST":

        forma = request.form["forma_pago"]
        subtotal = request.form["subtotal"]
        iva = request.form["total_iva"]
        descuento = request.form["total_descuento"]
        total = request.form["total_factura"]
        pagado = request.form["valor_pagado"]
        cambio = request.form["cambio_devuelto"]

        cursor.execute("""
            UPDATE factura
            SET
                forma_pago=%s,
                subtotal=%s,
                total_iva=%s,
                total_descuento=%s,
                total_factura=%s,
                valor_pagado=%s,
                cambio_devuelto=%s
            WHERE id_factura=%s
        """,
        (
            forma,
            subtotal,
            iva,
            descuento,
            total,
            pagado,
            cambio,
            id
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        return redirect("/facturas")

    cursor.execute("""
        SELECT
            id_factura,
            numero_factura_oficial,
            id_cliente,
            id_sede,
            id_empleado,
            forma_pago,
            subtotal,
            total_iva,
            total_descuento,
            total_factura,
            valor_pagado,
            cambio_devuelto
        FROM factura
        WHERE id_factura=%s
    """,(id,))

    factura = cursor.fetchone()

    cursor.close()
    conexion.close()

    return render_template(
        "editar_factura.html",
        factura=factura
    )


@app.route("/facturas/eliminar/<int:id>")
def eliminar_factura(id):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM factura
        WHERE id_factura=%s
    """,(id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return redirect("/facturas")
if __name__ == "__main__":
    app.run(debug=True)

