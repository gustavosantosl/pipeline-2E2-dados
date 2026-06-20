$ErrorActionPreference = "Stop"

Set-Location olist_pipeline

Write-Host ">>> Rodando models DBT..."
dbt run

Write-Host ">>> Rodando testes DBT..."
dbt test

Set-Location ..
Write-Host ">>> Tudo ok!"