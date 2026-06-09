WITH source AS (
  SELECT * FROM {{ source('olist_raw', 'raw_order_items') }}
)

SELECT
  order_id,
  order_item_id,
  product_id,
  seller_id,
  price AS preco_produto,
  freight_value AS valor_frete,
  (price + freight_value) AS valor_total_item
FROM source