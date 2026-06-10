SELECT
    c.customer_unique_id,
    c.estado_cliente,
    COUNT(DISTINCT o.order_id)   AS total_pedidos,
    ROUND(SUM(o.total_paid), 2)  AS valor_total,
    MAX(o.purchased_at)          AS ultimo_pedido,
    ROUND(AVG(r.review_score), 2) AS nota_media
FROM {{ ref('stg_customers') }} c
LEFT JOIN {{ ref('int_orders_enriched') }} o
    ON c.customer_id = o.customer_id
LEFT JOIN {{ ref('stg_reviews') }} r
    ON o.order_id = r.order_id
GROUP BY 1, 2