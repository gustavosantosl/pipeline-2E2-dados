WITH source AS (
  
  SELECT * FROM {{ source('olist_raw', 'raw_orders') }}
)

SELECT
  order_id,
  customer_id,
  order_status,
  order_purchase_timestamp::TIMESTAMP AS purchased_at,
  order_delivered_customer_date::TIMESTAMP AS delivered_at,
  order_estimated_delivery_date::TIMESTAMP AS estimated_at
FROM source