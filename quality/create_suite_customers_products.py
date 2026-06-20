import duckdb
import great_expectations as gx

context = gx.get_context(context_root_dir="gx")

# PARTE 1: SUÍTE PARA RAW_CUSTOMERS
print("Iniciando validação de RAW_CUSTOMERS...")

con = duckdb.connect(r"../data/olist.duckdb", read_only=True)
df_customers = con.execute("SELECT * FROM raw_customers").df()

try:
    ds_cust = context.data_sources.add_pandas("ds_customers")
except Exception:
    ds_cust = context.data_sources.get("ds_customers")

try:
    asset_cust = ds_cust.add_dataframe_asset("raw_customers")
except Exception:
    asset_cust = ds_cust.get_asset("raw_customers")

try:
    batch_def_cust = asset_cust.add_batch_definition_whole_dataframe("batch_cust")
except Exception:
    batch_def_cust = asset_cust.get_batch_definition("batch_cust")

try:
    suite_cust = context.suites.add(gx.ExpectationSuite(name="customers_suite"))
except Exception:
    suite_cust = context.suites.get("customers_suite")
    for exp in list(suite_cust.expectations): suite_cust.delete_expectation(exp)

# Regras Customers
suite_cust.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="customer_id"))
suite_cust.add_expectation(gx.expectations.ExpectColumnValueLengthsToEqual(column="customer_state", value=2))

suite_cust.save()
res_cust = batch_def_cust.get_batch(batch_parameters={"dataframe": df_customers}).validate(suite_cust)
print(f"✅ Customers passou: {res_cust.success}")


# PARTE 2: SUÍTE PARA RAW_PRODUCTS
print("\nIniciando validação de RAW_PRODUCTS...")

df_products = con.execute("SELECT * FROM raw_products").df()
con.close() # Fecha o banco

try:
    ds_prod = context.data_sources.add_pandas("ds_products")
except Exception:
    ds_prod = context.data_sources.get("ds_products")

try:
    asset_prod = ds_prod.add_dataframe_asset("raw_products")
except Exception:
    asset_prod = ds_prod.get_asset("raw_products")

try:
    batch_def_prod = asset_prod.add_batch_definition_whole_dataframe("batch_prod")
except Exception:
    batch_def_prod = asset_prod.get_batch_definition("batch_prod")

try:
    suite_prod = context.suites.add(gx.ExpectationSuite(name="products_suite"))
except Exception:
    suite_prod = context.suites.get("products_suite")
    for exp in list(suite_prod.expectations): suite_prod.delete_expectation(exp)

# Regra Products
# Regra Products com tolerância de 95%
suite_prod.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="product_category_name", mostly=0.97))
suite_prod.save()
res_prod = batch_def_prod.get_batch(batch_parameters={"dataframe": df_products}).validate(suite_prod)
print(f"✅ Products passou: {res_prod.success}")