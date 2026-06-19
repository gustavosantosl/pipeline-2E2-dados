import duckdb
import pandas as pd
import great_expectations as gx

con = duckdb.connect(r"../data/olist.duckdb", read_only=True)
df = con.execute("SELECT * FROM raw_orders").df()
con.close()

print(f"Linhas carregadas: {len(df)}")

context = gx.get_context(context_root_dir="gx")

datasource_name = "olist_pandas"
try:
    ds = context.data_sources.add_pandas(name=datasource_name)
except Exception:
    ds = context.data_sources.get(datasource_name)

asset_name = "raw_orders"
try:
    asset = ds.add_dataframe_asset(name=asset_name)
except Exception:
    asset = ds.get_asset(asset_name)

batch_definition_name = "raw_orders_batch"
try:
    batch_definition = asset.add_batch_definition_whole_dataframe(batch_definition_name)
except Exception:
    batch_definition = asset.get_batch_definition(batch_definition_name)

batch_parameters = {"dataframe": df}

suite_name = "orders_suite"
try:
    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))
except Exception:
    suite = context.suites.get(suite_name)
    for exp in list(suite.expectations):
        suite.delete_expectation(exp)

suite.add_expectation(gx.expectations.ExpectColumnToExist(column="order_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id"))
suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(column="order_id"))

suite.save()

batch = batch_definition.get_batch(batch_parameters=batch_parameters)
results = batch.validate(suite)

print("✅ Sucesso! Conectado ao DuckDB (via Pandas) e 'orders_suite' salva com 3 regras.")
print(f"Validação passou: {results.success}")

if not results.success:
    for result in results.results:
        if not result.success:
            print(f"❌ Falhou: {result.expectation_config.type}")
            print(result.result)