-- ======================================
-- CLIENTE
-- ======================================

-- Búsqueda rápida por nombre
CREATE INDEX idx_cliente_nombre
ON Cliente(nombres, apellidos);

-- ======================================
-- PROVEEDOR
-- ======================================

-- Búsqueda por nombre del proveedor
CREATE INDEX idx_proveedor_nombre
ON Proveedor(nombre_proveedor);

-- ======================================
-- PRODUCTOS
-- ======================================

-- Búsqueda por nombre
CREATE INDEX idx_producto_nombre
ON Productos(nombre_producto);

-- Búsqueda por marca
CREATE INDEX idx_producto_marca
ON Productos(marca);

-- Búsqueda por categoría
CREATE INDEX idx_producto_tipo
ON Productos(tipo_de_producto);

-- ======================================
-- INVENTARIO
-- ======================================

-- Consultas por producto
CREATE INDEX idx_inventario_producto
ON Inventario(id_producto);

-- Consultas por sede
CREATE INDEX idx_inventario_sede
ON Inventario(id_sede);

-- ======================================
-- FACTURA
-- ======================================

-- Consultas por cliente
CREATE INDEX idx_factura_cliente
ON Factura(id_cliente);

-- Consultas por empleado
CREATE INDEX idx_factura_empleado
ON Factura(id_empleado);

-- Consultas por sede
CREATE INDEX idx_factura_sede
ON Factura(id_sede);

-- Reportes por fecha
CREATE INDEX idx_factura_fecha
ON Factura(fecha_emision);

-- ======================================
-- DETALLE FACTURA
-- ======================================

-- Productos vendidos
CREATE INDEX idx_detalle_factura_producto
ON Detalle_Factura(id_producto);

-- Consultas por factura
CREATE INDEX idx_detalle_factura_factura
ON Detalle_Factura(id_factura);

-- ======================================
-- ÓRDENES DE PEDIDO
-- ======================================

-- Órdenes por proveedor
CREATE INDEX idx_orden_proveedor
ON Ordenes_Pedidos(nit_proveedor);

-- Órdenes por sede
CREATE INDEX idx_orden_sede
ON Ordenes_Pedidos(id_sede);

-- Historial por fecha
CREATE INDEX idx_orden_fecha
ON Ordenes_Pedidos(fecha_pedido);

-- Estado de la orden
CREATE INDEX idx_orden_estado
ON Ordenes_Pedidos(estado_pedido);

-- ======================================
-- DETALLES PEDIDOS
-- ======================================

-- Productos solicitados
CREATE INDEX idx_detalle_pedido_producto
ON Detalles_Pedidos(id_producto);

-- Consulta de detalles por orden
CREATE INDEX idx_detalle_pedido_orden
ON Detalles_Pedidos(id_orden_pedido);