WITH source AS (
  SELECT * FROM {{ source('olist_raw', 'raw_payments') }}
)

SELECT
  order_id,
  payment_sequential AS sequencia_pagamento,
  payment_type AS tipo_pagamento,
  payment_installments AS parcelas,
  payment_value AS valor_pagamento
FROM source
WHERE payment_value > 0