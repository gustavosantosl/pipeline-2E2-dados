import os
import sys
import duckdb
import great_expectations as gx
from logger import get_logger

logger = get_logger(__name__)


def run_quality_checks():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gx_path = os.path.join(script_dir, "..", "quality", "gx")
    db_path = os.path.join(script_dir, "..", "data", "olist.duckdb")

    context = gx.get_context(context_root_dir=gx_path)

    logger.info("Iniciando validação de qualidade de dados...")

    try:
        ds_orders = context.data_sources.get("olist_pandas")
        ds_cust = context.data_sources.get("ds_customers")
        ds_prod = context.data_sources.get("ds_products")

        asset_orders = ds_orders.get_asset("raw_orders")
        asset_cust = ds_cust.get_asset("raw_customers")
        asset_prod = ds_prod.get_asset("raw_products")

        batch_def_orders = asset_orders.get_batch_definition("raw_orders_batch")
        batch_def_cust = asset_cust.get_batch_definition("batch_cust")
        batch_def_prod = asset_prod.get_batch_definition("batch_prod")

        vd_orders = context.validation_definitions.get("vd_orders")
        vd_cust = context.validation_definitions.get("vd_customers")
        vd_prod = context.validation_definitions.get("vd_products")
    except Exception as e:
        logger.exception("Falha ao carregar configuração do Great Expectations: %s", e)
        raise

    try:
        con = duckdb.connect(db_path, read_only=True)
        df_orders = con.execute("SELECT * FROM raw_orders").df()
        df_cust = con.execute("SELECT * FROM raw_customers").df()
        df_prod = con.execute("SELECT * FROM raw_products").df()
        con.close()
    except Exception as e:
        logger.exception("Falha ao carregar dados do DuckDB: %s", e)
        raise

    logger.info("Dados carregados, iniciando validações...")

    res_orders = vd_orders.run(batch_parameters={"dataframe": df_orders})
    res_cust = vd_cust.run(batch_parameters={"dataframe": df_cust})
    res_prod = vd_prod.run(batch_parameters={"dataframe": df_prod})

    resultados = {
        "orders_suite": res_orders.success,
        "customers_suite": res_cust.success,
        "products_suite": res_prod.success,
    }

    passou_tudo = all(resultados.values())

    if not passou_tudo:
        logger.error("FALHA NA QUALIDADE DE DADOS!")
        for nome_suite, sucesso in resultados.items():
            status = "PASSOU" if sucesso else "FALHOU"
            logger.error("  -> %s: %s", nome_suite, status)
        sys.exit(1)

    logger.info("Qualidade OK: %s", resultados)
    return True


if __name__ == "__main__":
    run_quality_checks()