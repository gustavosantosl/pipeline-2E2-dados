WITH source AS (
  SELECT * FROM {{ source('olist_raw', 'raw_customers') }}
)

SELECT
  customer_id,
  customer_unique_id,
  customer_city AS cidade_cliente,
  customer_state AS estado_cliente,
  customer_zip_code_prefix AS cep_cliente
FROM source