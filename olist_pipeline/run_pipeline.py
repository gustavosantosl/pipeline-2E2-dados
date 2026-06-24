import subprocess
import sys

steps = [
    ('Ingestão', [sys.executable, 'ingestion/load.py']),
    ('Qualidade', [sys.executable, 'olist_pipeline/run_quality.py']),
    ('Transformação DBT', ['powershell', '-File', 'run_dbt.ps1']),
]

for name, cmd in steps:
    print(f'\n>>> {name}...')
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f'ERRO na etapa: {name}')
        sys.exit(1)

print('\nPipeline completo com sucesso!')