SELECT order_id, purchased_at
FROM {{ ref('stg_orders') }}
WHERE purchased_at > CURRENT_DATE