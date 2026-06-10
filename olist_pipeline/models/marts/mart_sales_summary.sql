WITH orders AS (
  SELECT * FROM {{ ref('int_orders_enriched') }}
),
items AS (
  SELECT oi.order_id, p.categoria_produto AS categoria,
    SUM(oi.preco_produto) as receita
  FROM {{ ref('stg_order_items') }} oi
  LEFT JOIN {{ ref('stg_products') }} p ON oi.product_id = p.product_id
  GROUP BY 1, 2
)
SELECT
  strftime(o.purchased_at, '%Y-%m') AS mes,
  i.categoria AS categoria,
  COUNT(DISTINCT o.order_id) AS total_pedidos,
  ROUND(SUM(i.receita), 2) AS receita_total
FROM orders o
LEFT JOIN items i ON o.order_id = i.order_id
GROUP BY 1, 2