WITH orders AS  (
    SELECT * FROM {{ ref('stg_orders') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
)

SELECT 
    orders.order_id,
    orders.order_status,
    customers.cidade_cliente,
    customers.estado_cliente
FROM orders
LEFT JOIN customers 
    ON orders.customer_id = customers.customer_id