import great_expectations as gx
import duckdb

context = gx.get_context(context_root_dir="gx")

print("Montando o checkpoint...")

ds_orders = context.data_sources.get("olist_pandas")
ds_cust = context.data_sources.get("ds_customers")
ds_prod = context.data_sources.get("ds_products")

asset_orders = ds_orders.get_asset("raw_orders")
asset_cust = ds_cust.get_asset("raw_customers")
asset_prod = ds_prod.get_asset("raw_products")

batch_def_orders = asset_orders.get_batch_definition("raw_orders_batch")
batch_def_cust = asset_cust.get_batch_definition("batch_cust")
batch_def_prod = asset_prod.get_batch_definition("batch_prod")

suite_orders = context.suites.get("orders_suite")
suite_cust = context.suites.get("customers_suite")
suite_prod = context.suites.get("products_suite")

try:
    vd_orders = context.validation_definitions.add(
        gx.ValidationDefinition(name="vd_orders", data=batch_def_orders, suite=suite_orders)
    )
except Exception:
    vd_orders = context.validation_definitions.get("vd_orders")

try:
    vd_cust = context.validation_definitions.add(
        gx.ValidationDefinition(name="vd_customers", data=batch_def_cust, suite=suite_cust)
    )
except Exception:
    vd_cust = context.validation_definitions.get("vd_customers")

try:
    vd_prod = context.validation_definitions.add(
        gx.ValidationDefinition(name="vd_products", data=batch_def_prod, suite=suite_prod)
    )
except Exception:
    vd_prod = context.validation_definitions.get("vd_products")

try:
    checkpoint = context.checkpoints.add(
        gx.Checkpoint(name="olist_checkpoint", validation_definitions=[vd_orders, vd_cust, vd_prod])
    )
except Exception:
    checkpoint = context.checkpoints.get("olist_checkpoint")

print("Carregando os dados...")
con = duckdb.connect(r"../data/olist.duckdb", read_only=True)
df_orders = con.execute("SELECT * FROM raw_orders").df()
df_cust = con.execute("SELECT * FROM raw_customers").df()
df_prod = con.execute("SELECT * FROM raw_products").df()
con.close()

print("\nRodando as validações...")

res_orders = vd_orders.run(batch_parameters={"dataframe": df_orders})
res_cust = vd_cust.run(batch_parameters={"dataframe": df_cust})
res_prod = vd_prod.run(batch_parameters={"dataframe": df_prod})

resultados = {
    "orders_suite": res_orders.success,
    "customers_suite": res_cust.success,
    "products_suite": res_prod.success,
}

passou_tudo = all(resultados.values())

print("\n--- Resultado do olist_checkpoint ---")
for nome_suite, sucesso in resultados.items():
    print(f" -> {nome_suite}: {'✅ PASSOU' if sucesso else '❌ FALHOU'}")

print(f"\n RESULTADO GERAL DO PIPELINE: {passou_tudo}")