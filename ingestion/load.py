import duckdb
con = duckdb.connect(r'data/olist.duckdb')

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
for table, path in files.items():
    con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto('data-raw/{path}')")
    print(f'{table}: OK')

print("Ingestão finalizada! Dados salvos no olist.duckdb.")
con.close()