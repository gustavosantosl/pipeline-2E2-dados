WITH source AS (
  SELECT * FROM {{ source('olist_raw', 'raw_products') }}
)

SELECT
  product_id,
  product_category_name AS categoria_produto,
  COALESCE(product_name_lenght, 0)::INT AS tamanho_nome_produto,
  COALESCE(product_description_lenght, 0)::INT AS tamanho_descricao_produto,
  COALESCE(product_photos_qty, 0)::INT AS qtd_fotos_produto
FROM source