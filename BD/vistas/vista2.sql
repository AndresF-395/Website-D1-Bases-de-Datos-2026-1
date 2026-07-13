-- ==========================================
-- Vista general del inventario por sede
-- ==========================================


CREATE OR REPLACE VIEW vista_inventario_productos AS


SELECT

    p.id_producto,

    p.codigo_de_barras,

    p.nombre_producto,

    p.marca,

    p.tipo_de_producto,


    s.id_sede,

    s.nombre_sede,


    i.cantidad_disponible,

    i.stock_minimo,

    i.stock_maximo


FROM Inventario i


INNER JOIN Productos p
ON i.id_producto = p.id_producto


INNER JOIN Sedes s
ON i.id_sede = s.id_sede;