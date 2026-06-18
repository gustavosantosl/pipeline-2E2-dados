SELECT 
    order_id, 
    valor_pagamento
FROM {{ ref('stg_payments') }}
WHERE valor_pagamento <= 0