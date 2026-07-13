-- ==========================================
-- Vista de órdenes realizadas a proveedores
-- ==========================================


CREATE OR REPLACE VIEW vista_ordenes_proveedores AS


SELECT

    o.id_orden_pedido,

    o.fecha_pedido,

    p.nit_proveedor,

    p.nombre_proveedor,

    s.nombre_sede,

    o.estado_pedido,

    o.total,

    o.lugar_entrega


FROM Ordenes_Pedidos o


INNER JOIN Proveedor p
ON o.nit_proveedor = p.nit_proveedor


INNER JOIN Sedes s
ON o.id_sede = s.id_sede;