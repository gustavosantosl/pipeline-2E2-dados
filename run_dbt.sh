#!/bin/bash
# run_dbt.sh
set -e

cd olist_pipeline

echo '>>> Rodando models DBT...'
dbt run

echo '>>> Rodando testes DBT...'
dbt test

cd ..
echo '>>> Tudo ok!'