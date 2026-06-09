WITH source AS
( SELECT * FROM {{ source('olist_raw', 'raw_sellers') }}
)
SELECT 
    seller_id AS id_vendedor,
    seller_zip_code_prefix AS cep_vendedor,
    seller_city AS cidade_vendedor,
    seller_state AS estado_vendedor
FROM source

