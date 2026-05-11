-- 1. JOIN entre pedidos e clientes (Amostra)
SELECT 
    o.order_id, 
    o.order_status, 
    c.customer_state
FROM raw_orders o
JOIN raw_customers c ON o.customer_id = c.customer_id
LIMIT 10;

-- 2. Ticket médio e quantidade de pedidos por categoria
SELECT
  p.product_category_name,
  COUNT(oi.order_id) as qtd_pedidos,
  ROUND(AVG(oi.price), 2) as ticket_medio
FROM raw_order_items oi
JOIN raw_products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY qtd_pedidos DESC
LIMIT 15;

-- 3. Tempo médio de entrega em dias
SELECT 
    ROUND(AVG(date_diff('day', order_purchase_timestamp, order_delivered_customer_date)), 1) AS media_dias_entrega
FROM raw_orders
WHERE order_status = 'delivered';