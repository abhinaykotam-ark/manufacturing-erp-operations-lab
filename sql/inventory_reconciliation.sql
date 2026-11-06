
-- ERP inventory reconciliation
-- Read-only queries against Odoo PostgreSQL

-- 1. Raw materials and finished goods
SELECT
    pp.default_code AS product_code,
    sl.name AS location,
    SUM(sq.quantity) AS on_hand
FROM stock_quant sq
JOIN product_product pp
    ON sq.product_id = pp.id
JOIN stock_location sl
    ON sq.location_id = sl.id
WHERE pp.default_code IN ('RESISTOR-10K', 'ASSEMBLY-001')
  AND sl.usage = 'internal'
GROUP BY pp.default_code, sl.name
ORDER BY pp.default_code;

-- 2. Quality Hold reconciliation
SELECT
    COALESCE(SUM(CASE WHEN sl.name = 'Stock'
        THEN sq.quantity ELSE 0 END), 0) AS regular_stock,
    COALESCE(SUM(CASE WHEN sl.name = 'Quality Hold'
        THEN sq.quantity ELSE 0 END), 0) AS quality_hold,
    COALESCE(SUM(sq.quantity), 0) AS total_inventory
FROM stock_quant sq
JOIN product_product pp
    ON sq.product_id = pp.id
JOIN stock_location sl
    ON sq.location_id = sl.id
WHERE pp.default_code = 'ASSEMBLY-001'
  AND sl.usage = 'internal';
