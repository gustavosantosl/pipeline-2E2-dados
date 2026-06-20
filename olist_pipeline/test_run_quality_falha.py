import duckdb
import great_expectations as gx
import sys


def run_quality_checks_com_falha_simulada():
    context = gx.get_context(context_root_dir="../quality/gx")

    ds_orders = context.data_sources.get("olist_pandas")
    asset_orders = ds_orders.get_asset("raw_orders")
    batch_def_orders = asset_orders.get_batch_definition("raw_orders_batch")
    suite_orders = context.suites.get("orders_suite")
    vd_orders = context.validation_definitions.get("vd_orders")

    # Carrega os dados reais...
    con = duckdb.connect(r"../data/olist.duckdb", read_only=True)
    df_orders = con.execute("SELECT * FROM raw_orders").df()
    con.close()

    # ...e ESTRAGA DE PROPÓSITO só na cópia em memória (não toca no banco real)
    print("⚠️  Simulando dado inválido: duplicando o primeiro order_id...")
    df_orders_quebrado = df_orders.copy()
    df_orders_quebrado.loc[1, "order_id"] = df_orders_quebrado.loc[0, "order_id"]

    res_orders = vd_orders.run(batch_parameters={"dataframe": df_orders_quebrado})

    resultados = {"orders_suite": res_orders.success}
    passou_tudo = all(resultados.values())

    if not passou_tudo:
        print("❌ FALHA NA QUALIDADE DE DADOS!")
        for nome_suite, sucesso in resultados.items():
            status = "✅ PASSOU" if sucesso else "❌ FALHOU"
            print(f"  -> {nome_suite}: {status}")
        sys.exit(1)

    print(f"✅ Qualidade OK: {resultados}")
    return True


if __name__ == "__main__":
    run_quality_checks_com_falha_simulada()