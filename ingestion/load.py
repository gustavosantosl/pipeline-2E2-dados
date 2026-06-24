import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
pipeline_dir = os.path.join(script_dir, "..", "olist_pipeline")
sys.path.append(pipeline_dir)

from logger import get_logger
import duckdb

logger = get_logger(__name__)

db_path = os.path.join(script_dir, "..", "data", "olist.duckdb")
data_raw_path = os.path.join(script_dir, "..", "data-raw")

con = duckdb.connect(db_path)

files = {
    'raw_orders': 'olist_orders_dataset.csv',
    'raw_customers': 'olist_customers_dataset.csv',
    'raw_products': 'olist_products_dataset.csv',
    'raw_order_items': 'olist_order_items_dataset.csv',
    'raw_payments': 'olist_order_payments_dataset.csv',
    'raw_reviews': 'olist_order_reviews_dataset.csv',
    'raw_sellers': 'olist_sellers_dataset.csv',
    'raw_geolocation': 'olist_geolocation_dataset.csv',
    'raw_category_translation': 'product_category_name_translation.csv'
}

logger.info("Iniciando ingestão...")

for table, filename in files.items():
    csv_path = os.path.join(data_raw_path, filename).replace("\\", "/")
    try:
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto('{csv_path}')")
        logger.info("%s: OK", table)
    except Exception as e:
        logger.exception("Falha ao carregar tabela %s: %s", table, e)
        con.close()
        raise

logger.info("Ingestão concluída: %d tabelas carregadas", len(files))
con.close()