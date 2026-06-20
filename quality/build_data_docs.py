import great_expectations as gx

context = gx.get_context(context_root_dir="gx")

print("Gerando Data Docs...")
context.build_data_docs()

print("Abrindo no navegador...")
context.open_data_docs()