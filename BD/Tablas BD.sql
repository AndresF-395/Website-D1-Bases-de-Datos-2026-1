-- ======================================
-- ELIMINACIÓN
-- ======================================

DROP TABLE IF EXISTS Detalles_Pedidos CASCADE;
DROP TABLE IF EXISTS Ordenes_Pedidos CASCADE;
DROP TABLE IF EXISTS Turnos CASCADE;
DROP TABLE IF EXISTS Detalle_Factura CASCADE;
DROP TABLE IF EXISTS Factura CASCADE;
DROP TABLE IF EXISTS Inventario CASCADE;
DROP TABLE IF EXISTS Empleados CASCADE;
DROP TABLE IF EXISTS Sedes CASCADE;
DROP TABLE IF EXISTS Productos_Por_Proveedor CASCADE;
DROP TABLE IF EXISTS Productos CASCADE;
DROP TABLE IF EXISTS Proveedor CASCADE;
DROP TABLE IF EXISTS Cliente CASCADE;
DROP TABLE IF EXISTS Residente CASCADE;
DROP TABLE IF EXISTS Ciudad CASCADE;
DROP TABLE IF EXISTS Tipos_Turno CASCADE;
DROP TABLE IF EXISTS Departamentos CASCADE;
-- ======================================
-- DEPARTAMENTOS
-- ======================================

CREATE TABLE Departamentos(
    id_departamento SERIAL PRIMARY KEY,
    nombre_departamento VARCHAR(50) UNIQUE NOT NULL
);

-- ======================================
-- TIPOS TURNO
-- ======================================

CREATE TABLE Tipos_Turno(
    id_tipo_turno SERIAL PRIMARY KEY,
    nombre_turno VARCHAR(30) NOT NULL,
    hora_apertura TIME NOT NULL,
    hora_cierre TIME NOT NULL
);

-- ======================================
-- CIUDAD
-- ======================================

CREATE TABLE Ciudad(
    id_ciudad SERIAL PRIMARY KEY,
    nombre_ciudad VARCHAR(50) UNIQUE NOT NULL,
    codigo_postal VARCHAR(10) UNIQUE NOT NULL,
    id_departamento INT NOT NULL,

    FOREIGN KEY(id_departamento)
    REFERENCES Departamentos(id_departamento)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,

    CONSTRAINT chk_codigo_postal_len
    CHECK (LENGTH(codigo_postal)>=4)
);

-- ======================================
-- CLIENTE
-- ======================================

CREATE TABLE Cliente(
    id_cliente SERIAL PRIMARY KEY,
    tipo_documento VARCHAR(5) NOT NULL
    CHECK(tipo_documento IN ('CC','CE','NIT','PP','TI')),

    numero_documento VARCHAR(20) NOT NULL,
    nombres VARCHAR(50) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    telefono_cliente VARCHAR(15),
    correo_cliente VARCHAR(100) UNIQUE,
    direccion_residencia VARCHAR(150),
    habeas_data BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT uq_documento_cliente
    UNIQUE(tipo_documento,numero_documento)
);

-- ======================================
-- PROVEEDOR
-- ======================================

CREATE TABLE Proveedor(
    nit_proveedor VARCHAR(20) PRIMARY KEY,
    nombre_proveedor VARCHAR(100) NOT NULL,
    direccion_empresa VARCHAR(150) NOT NULL,
    telefono_proveedor VARCHAR(15),
    correo_proveedor VARCHAR(100) UNIQUE,
    --Nuevos atributos
    rut VARCHAR(50),
    certificacion_bancaria VARCHAR(150),
    tipo_proveedor VARCHAR(50),
    tiempo_entrega_promedio INT CHECK(tiempo_entrega_promedio >= 0), -- Expresado en días
    contacto_comercial VARCHAR(100),
    contacto_cartera VARCHAR(100),
    contacto_logistico VARCHAR(100),
    condiciones_pago VARCHAR(100),
    calificacion INT CHECK(calificacion BETWEEN 1 AND 5)
);

-- ======================================
-- PRODUCTOS
-- ======================================

CREATE TABLE Productos(
    id_producto SERIAL PRIMARY KEY,
    codigo_de_barras VARCHAR(30) UNIQUE NOT NULL,
    nombre_producto VARCHAR(80) NOT NULL,
    tipo_de_producto VARCHAR(50) NOT NULL,

    precio_compra NUMERIC(12,2)
    NOT NULL CHECK(precio_compra>0),

    precio_venta NUMERIC(12,2)
    NOT NULL CHECK(precio_venta>0),

    marca VARCHAR(50) NOT NULL,
    fecha_vencimiento DATE,

    tipo_iva VARCHAR(15)
    DEFAULT 'EXCLUIDO'
    CHECK(tipo_iva IN
    ('GENERAL','DIFERENCIAL','EXENTO','EXCLUIDO')),

    activo BOOLEAN DEFAULT TRUE,
    --Nuevo atributo
    demanda_diaria INT DEFAULT 0 CHECK(demanda_diaria >= 0),

    CONSTRAINT chk_margen_operativo
    CHECK(precio_venta>=precio_compra)
);

-- ======================================
-- PRODUCTOS POR PROVEEDOR (Nueva)
-- ======================================

CREATE TABLE Productos_Por_Proveedor(
    id_producto_proveedor SERIAL PRIMARY KEY,
    nit_proveedor VARCHAR(20) NOT NULL,
    codigo_producto INT NOT NULL, -- FK hacia Productos
    
    precio_compra NUMERIC(12,2) NOT NULL CHECK(precio_compra > 0),
    fecha_inicio_suministro DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_fin_suministro DATE,
    activo BOOLEAN DEFAULT TRUE,
    observaciones VARCHAR(255),
    
    FOREIGN KEY(nit_proveedor) 
    REFERENCES Proveedor(nit_proveedor) ON DELETE CASCADE,
    
    FOREIGN KEY(codigo_producto) 
    REFERENCES Productos(id_producto) ON DELETE CASCADE
);  

-- ======================================
-- SEDES
-- ======================================

CREATE TABLE Sedes(
    id_sede SERIAL PRIMARY KEY,
    nombre_sede VARCHAR(50) NOT NULL,
    barrio_sede VARCHAR(50) NOT NULL,
    id_ciudad INT NOT NULL,
    direccion VARCHAR (100) UNIQUE NOT NULL,

    horario_atencion_apertura TIME NOT NULL,
    horario_atencion_cierre TIME NOT NULL,

    FOREIGN KEY(id_ciudad)
    REFERENCES Ciudad(id_ciudad)
);

-- ======================================
-- EMPLEADOS
-- ======================================

CREATE TABLE Empleados(
    id_empleado SERIAL PRIMARY KEY,
    cedula_empleado VARCHAR(20) UNIQUE NOT NULL,
    nombre_empleado VARCHAR(50) NOT NULL,
    apellido_empleado VARCHAR(50) NOT NULL,

    fecha_nacimiento DATE NOT NULL,

    cargo VARCHAR(30) NOT NULL,

    salario NUMERIC(12,2)
    NOT NULL CHECK(salario>0),

    fecha_contrato DATE DEFAULT CURRENT_DATE,

    telefono_empleado VARCHAR(15),
    correo_empleado VARCHAR(100) UNIQUE,

    id_sede INT NOT NULL,

    FOREIGN KEY(id_sede)
    REFERENCES Sedes(id_sede),

    CHECK(
        fecha_nacimiento <=
        CURRENT_DATE - INTERVAL '18 years'
    )
);

-- ======================================
-- INVENTARIO
-- ======================================

CREATE TABLE Inventario(
    id_inventario SERIAL PRIMARY KEY,

    id_producto INT NOT NULL,
    id_sede INT NOT NULL,

    cantidad_disponible INT
    DEFAULT 0 CHECK(cantidad_disponible>=0),

    stock_minimo INT
    DEFAULT 10 CHECK(stock_minimo>=0),

    stock_maximo INT DEFAULT 1000,

    FOREIGN KEY(id_producto)
    REFERENCES Productos(id_producto),

    FOREIGN KEY(id_sede)
    REFERENCES Sedes(id_sede),

    UNIQUE(id_producto,id_sede),

    CHECK(stock_maximo>=stock_minimo)
);

-- ======================================
-- FACTURA
-- ======================================

CREATE TABLE Factura(
    id_factura SERIAL PRIMARY KEY,
    numero_factura_oficial VARCHAR(50)
    UNIQUE NOT NULL,

    id_cliente INT NOT NULL,
    id_sede INT NOT NULL,
    id_empleado INT NOT NULL,

    fecha_emision TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    forma_pago VARCHAR(20) NOT NULL
    CHECK(forma_pago IN
    ('EFECTIVO','DEBITO','CREDITO','BONO')),

    subtotal NUMERIC(12,2) NOT NULL
    DEFAULT 0 CHECK(subtotal>=0),

    total_iva NUMERIC(12,2) NOT NULL
    DEFAULT 0 CHECK(total_iva>=0),

    total_descuento NUMERIC(12,2) NOT NULL
    DEFAULT 0 CHECK(total_descuento>=0),

    total_factura NUMERIC(12,2) NOT NULL
    DEFAULT 0 CHECK(total_factura>=0),

    valor_pagado NUMERIC(12,2) NOT NULL
    CHECK(valor_pagado>=0),

    cambio_devuelto NUMERIC(12,2) NOT NULL
    DEFAULT 0 CHECK(cambio_devuelto>=0),

    FOREIGN KEY(id_cliente)
    REFERENCES Cliente(id_cliente),

    FOREIGN KEY(id_sede)
    REFERENCES Sedes(id_sede),

    FOREIGN KEY(id_empleado)
    REFERENCES Empleados(id_empleado),

    CHECK(valor_pagado>=total_factura)
);

-- ======================================
-- DETALLE FACTURA
-- ======================================

CREATE TABLE Detalle_Factura(
    id_linea SERIAL PRIMARY KEY,

    id_factura INT NOT NULL,
    id_producto INT NOT NULL,

    cantidad INT NOT NULL
    CHECK(cantidad>0),

    precio_unitario_aplicado NUMERIC(12,2) NOT NULL
    CHECK(precio_unitario_aplicado>=0),

    subtotal_linea NUMERIC(12,2) NOT NULL
    CHECK(subtotal_linea>=0),

    iva_aplicado NUMERIC(12,2) NOT NULL,

    FOREIGN KEY(id_factura)
    REFERENCES Factura(id_factura)
    ON DELETE CASCADE,

    FOREIGN KEY(id_producto)
    REFERENCES Productos(id_producto),

    UNIQUE(id_factura,id_producto)
);

-- ======================================
-- TURNOS
-- ======================================

CREATE TABLE Turnos(
    id_turno SERIAL PRIMARY KEY,
    id_empleado INT NOT NULL,
    id_tipo_turno INT NOT NULL,

    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,

    FOREIGN KEY(id_empleado)
    REFERENCES Empleados(id_empleado),

    FOREIGN KEY(id_tipo_turno)
    REFERENCES Tipos_Turno(id_tipo_turno)
);

-- ======================================
-- ORDENES
-- ======================================

CREATE TABLE Ordenes_Pedidos(
    id_orden_pedido SERIAL PRIMARY KEY,

    nit_proveedor VARCHAR(20) NOT NULL,
    id_sede INT NOT NULL,

    fecha_pedido TIMESTAMP
    DEFAULT CURRENT_TIMESTAMP,

    estado_pedido VARCHAR(20)
    DEFAULT 'PENDIENTE'
    CHECK(
    estado_pedido IN
    ('PENDIENTE','APROBADO',
    'RECIBIDO','RECHAZADO')
    ),

    total NUMERIC(12,2)
    DEFAULT 0 CHECK(total>=0),

    lugar_entrega VARCHAR(150),
    codigo_producto INT, -- FK hacia Productos
    
    FOREIGN KEY(codigo_producto)
    REFERENCES Productos(id_producto),

    FOREIGN KEY(nit_proveedor)
    REFERENCES Proveedor(nit_proveedor),

    FOREIGN KEY(id_sede)
    REFERENCES Sedes(id_sede)
);

-- ======================================
-- DETALLES PEDIDOS
-- ======================================

CREATE TABLE Detalles_Pedidos(
    id_detalle_pedido SERIAL PRIMARY KEY,

    id_orden_pedido INT NOT NULL,
    id_producto INT NOT NULL,

    cantidad INT
    CHECK(cantidad>0),

    precio_compra_unitario NUMERIC(12,2)
    CHECK(precio_compra_unitario>0),

    subtotal_pedido NUMERIC(12,2)
    CHECK(subtotal_pedido>0),

    FOREIGN KEY(id_orden_pedido)
    REFERENCES Ordenes_Pedidos(id_orden_pedido)
    ON DELETE CASCADE,

    FOREIGN KEY(id_producto)
    REFERENCES Productos(id_producto),

    UNIQUE(id_orden_pedido,id_producto)
);

-- ======================================
-- FUNCIÓN Y TRIGGER PARA INVENTARIO
-- ======================================

/*
 * REQUERIMIENTOS 6, 7 Y 9:
 * Función PL/pgSQL que se encarga de reducir el inventario tomando en cuenta la sede 
 * (desde la Factura maestra) y respetando las fechas para no alterar el historial.
 */
CREATE OR REPLACE FUNCTION fx_actualizar_inventario_venta()
RETURNS TRIGGER AS $$
DECLARE
    v_id_sede INT;
    v_fecha_emision TIMESTAMP;
    v_stock_actual INT;
BEGIN
    -- 1. Identificar la sede y la fecha de la venta desde la tabla maestra
    SELECT id_sede, fecha_emision
    INTO v_id_sede, v_fecha_emision
    FROM Factura
    WHERE id_factura = NEW.id_factura;

    -- 2. Restricción de fecha: Solo afectar inventario si la factura es actual o futura
    -- DATE() convierte el timestamp a fecha simple para comparar correctamente con CURRENT_DATE
    IF DATE(v_fecha_emision) >= CURRENT_DATE THEN
        
        -- 3. Identificar cantidad disponible del producto en la sede correspondiente
        SELECT cantidad_disponible
        INTO v_stock_actual
        FROM Inventario
        WHERE id_producto = NEW.id_producto AND id_sede = v_id_sede;
        
        -- Validación: El producto debe existir en el inventario de la sede
        IF NOT FOUND THEN
            RAISE EXCEPTION 'El producto con ID % no está configurado en el inventario de la sede %.', NEW.id_producto, v_id_sede;
        END IF;
        
        -- 4. Validación para prevenir stock negativo
        IF v_stock_actual < NEW.cantidad THEN
            RAISE EXCEPTION 'Stock insuficiente para el producto ID %. Disponible: %, Solicitado: %', NEW.id_producto, v_stock_actual, NEW.cantidad;
        END IF;
        
        -- 5. Efectuar el descuento en el inventario correspondiente
        UPDATE Inventario
        SET cantidad_disponible = cantidad_disponible - NEW.cantidad
        WHERE id_producto = NEW.id_producto AND id_sede = v_id_sede;
        
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger configurado AFTER INSERT para asegurar que el registro base haya guardado
CREATE TRIGGER trg_descontar_inventario
AFTER INSERT ON Detalle_Factura
FOR EACH ROW
EXECUTE FUNCTION fx_actualizar_inventario_venta();


/* Nueva función para el siguiente requisito: 
*Usando PL/pgSQL implementar gestión automática del inventario de productos / insumos.
* De modo que cuando se realicen órdenes de pedido se actualice el stock.
*/
CREATE OR REPLACE FUNCTION fx_actualizar_inventario_pedido()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_sede INT;
BEGIN

    -- Obtener la sede asociada a la orden
    SELECT id_sede
    INTO v_id_sede
    FROM Ordenes_Pedidos
    WHERE id_orden_pedido = NEW.id_orden_pedido;

    -- Verificar que exista el registro en inventario
    IF NOT EXISTS (
        SELECT 1
        FROM Inventario
        WHERE id_producto = NEW.id_producto
          AND id_sede = v_id_sede
    ) THEN
        RAISE EXCEPTION
            'No existe registro de inventario para el producto % en la sede %.',
            NEW.id_producto,
            v_id_sede;
    END IF;

    -- Aumentar el stock disponible
    UPDATE Inventario
    SET cantidad_disponible = cantidad_disponible + NEW.cantidad
    WHERE id_producto = NEW.id_producto
      AND id_sede = v_id_sede;

    RETURN NEW;

END;
$$;

--Trigger correspondiente a la última función agregada
CREATE TRIGGER trg_actualizar_inventario_pedido
AFTER INSERT
ON Detalles_Pedidos
FOR EACH ROW
EXECUTE FUNCTION fx_actualizar_inventario_pedido();
