-- 1. Quantos pedidos por status?
SELECT order_status, COUNT(*) as total
FROM raw_orders
GROUP BY order_status
ORDER BY total DESC;

-- 2. Qual estado tem mais clientes?
SELECT customer_state, COUNT(*) as clientes
FROM raw_customers
GROUP BY customer_state
ORDER BY clientes DESC
LIMIT 10;

-- 3. Qual o produto mais vendido?
SELECT product_id, COUNT(*) as quantidade_vendida
FROM raw_order_items
GROUP BY product_id
ORDER BY quantidade_vendida DESC
LIMIT 5;