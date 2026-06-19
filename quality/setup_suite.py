import great_expectations as gx

context = gx.get_context(context_root_dir="gx")

suite_name = "suite_dados_brutos"
try:
    suite = context.suites.add(gx.ExpectationSuite(name=suite_name))
except Exception:
    suite = context.suites.get(suite_name)

print(f"✅ Sucesso! A Expectation Suite '{suite_name}' foi criada e salva.")