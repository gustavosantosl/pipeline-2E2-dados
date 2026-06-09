WITH source AS (
  SELECT * FROM {{ source('olist_raw', 'raw_reviews') }}
)
SELECT
  review_id,
  order_id,
  review_score,
  COALESCE(review_comment_title, '') AS review_title,
  COALESCE(review_comment_message, '') AS review_message,
  review_creation_date::DATE AS review_date
FROM source
