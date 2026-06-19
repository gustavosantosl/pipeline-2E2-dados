import great_expectations as gx

context = gx.get_context(context_root_dir="gx")

datasource_name = "source_dados_brutos"
try:
    datasource = context.data_sources.add_pandas_filesystem(
        name=datasource_name,
        base_directory="../data-raw",
    )
except Exception:
    datasource = context.data_sources.get(datasource_name)

print(f"✅ Sucesso! O Datasource '{datasource_name}' foi mapeado e salvo.")