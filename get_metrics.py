import duckdb

# Conecta no nosso banco blindado
con = duckdb.connect(r"data/olist.duckdb", read_only=True)

print("\n📊 --- MÉTRICAS PARA O README --- 📊\n")

# 1. Pico de Receita (Agrupa pagamentos por mês/ano dos pedidos entregues)
query_receita = """
    SELECT 
        strftime(order_purchase_timestamp, '%Y-%m') as mes, 
        SUM(payment_value) as total_receita
    FROM raw_orders o
    JOIN raw_payments p ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY 1
    ORDER BY total_receita DESC
    LIMIT 1;
"""
res_receita = con.execute(query_receita).fetchone()
if res_receita:
    print(f"🏆 Pico de Receita: O mês com maior faturamento foi {res_receita[0]} (R$ {res_receita[1]:,.2f})")

# 2. Número de avaliações nota 5
query_reviews = "SELECT COUNT(*) FROM raw_reviews WHERE review_score = 5"
res_reviews = con.execute(query_reviews).fetchone()
if res_reviews:
    print(f"⭐ Satisfação: A grande maioria avalia com nota 5 (exatas {res_reviews[0]} avaliações)")

con.close()
print("\n==========================================\n")