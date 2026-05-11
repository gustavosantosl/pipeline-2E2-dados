import duckdb
import pandas

con = duckdb.connect(r'data/olist.duckdb')

print("Gerando insights de negócio...\n" + "-"*30)

import duckdb
import pandas as pd
from pathlib import Path

# 1. Conexão robusta com o banco de dados
pasta_raiz = Path(__file__).parent.parent
con = duckdb.connect(str(pasta_raiz / 'data' / 'olist.duckdb'))

print("Gerando insights de negócio...\n" + "-"*30)

# ==========================================
# INSIGHT 1: Receita por mês
# ==========================================
query_receita = """
  SELECT
    strftime(order_purchase_timestamp, '%Y-%m') as mes,
    SUM(payment_value) as receita
  FROM raw_orders o
  JOIN raw_payments p ON o.order_id = p.order_id
  GROUP BY mes 
  ORDER BY mes
"""
receita_mensal = con.execute(query_receita).df()

print("\n1. RECEITA MENSAL (Últimos 12 meses):")
# Usamos o tail(12) do Pandas para ver apenas o finalzinho da tabela
print(receita_mensal.tail(12)) 


# ==========================================
# INSIGHT 2: Top 5 Categorias por Receita
# ==========================================
query_categorias = """
  SELECT
    t.product_category_name_english as categoria,
    SUM(oi.price) as receita_total
  FROM raw_order_items oi
  JOIN raw_products p ON oi.product_id = p.product_id
  JOIN raw_category_translation t ON p.product_category_name = t.product_category_name
  GROUP BY categoria
  ORDER BY receita_total DESC
  LIMIT 5
"""
top_categorias = con.execute(query_categorias).df()

print("\n2. TOP 5 CATEGORIAS POR RECEITA:")
print(top_categorias)


# ==========================================
# INSIGHT 3: Distribuição de notas de review
# ==========================================
query_reviews = """
  SELECT
    review_score as nota,
    COUNT(*) as quantidade_avaliacoes
  FROM raw_reviews
  GROUP BY nota
  ORDER BY nota DESC
"""
distribuicao_reviews = con.execute(query_reviews).df()

print("\n3. DISTRIBUIÇÃO DE NOTAS DE REVIEW:")
print(distribuicao_reviews)

con.close()

