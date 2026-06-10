WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

payments AS (
    SELECT
        order_id,
        SUM(valor_pagamento) AS total_paid
    FROM {{ ref('stg_payments') }}
    GROUP BY order_id
)

SELECT
    orders.order_id,
    orders.customer_id,                       
    customers.customer_unique_id,              
    orders.purchased_at,
    orders.order_status,
    customers.cidade_cliente,
    customers.estado_cliente,
    COALESCE(payments.total_paid, 0) AS total_paid  
FROM orders
LEFT JOIN customers
    ON orders.customer_id = customers.customer_id
LEFT JOIN payments
    ON orders.order_id = payments.order_id