-- ======================================
-- 07_vista_dias_stock.sql
-- Vista: Días de Stock Disponible
-- ======================================

DROP VIEW IF EXISTS vista_dias_stock;

CREATE VIEW vista_dias_stock AS
SELECT
    i.id_inventario,
    s.id_sede,
    s.nombre_sede,
    p.id_producto,
    p.codigo_de_barras,
    p.nombre_producto,
    p.marca,

    i.cantidad_disponible,
    i.stock_minimo,
    i.stock_maximo,

    p.demanda_diaria,

    CASE
        WHEN p.demanda_diaria > 0 THEN
            ROUND((i.cantidad_disponible::NUMERIC / p.demanda_diaria), 2)
        ELSE
            NULL
    END AS dias_stock,

    CASE
        WHEN p.demanda_diaria = 0 THEN 'SIN DEMANDA'
        WHEN (i.cantidad_disponible::NUMERIC / p.demanda_diaria) < 3 THEN 'CRÍTICO'
        WHEN (i.cantidad_disponible::NUMERIC / p.demanda_diaria) BETWEEN 3 AND 7 THEN 'BAJO'
        ELSE 'SUFICIENTE'
    END AS estado_stock

FROM Inventario i
INNER JOIN Productos p
    ON i.id_producto = p.id_producto
INNER JOIN Sedes s
    ON i.id_sede = s.id_sede;