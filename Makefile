.PHONY: ingest quality transform pipeline docs clean help

ingest:
	python ingestion/load.py

quality:
	python olist_pipeline/run_quality.py

transform:
	powershell -File run_dbt.ps1

pipeline: ingest quality transform
	cd olist_pipeline && dbt docs generate

docs:
	cd olist_pipeline && dbt docs generate

clean:
	rm -f data/olist.duckdb

help:
	@echo "make ingest    - carrega CSVs no DuckDB"
	@echo "make quality   - valida qualidade dos dados"
	@echo "make transform - roda DBT"
	@echo "make pipeline  - roda tudo (ingest + quality + transform + docs)"
	@echo "make docs      - gera a documentacao do dbt"
	@echo "make clean     - remove o banco de dados DuckDB"