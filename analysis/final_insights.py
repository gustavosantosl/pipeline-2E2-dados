import os
import duckdb

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "..", "data", "olist.duckdb")

con = duckdb.connect(db_path, read_only=True)

print("=" * 60)
print("INSIGHT 1: Top 5 meses por receita")
print("=" * 60)
insight_1 = con.execute("""
    SELECT mes, SUM(receita_total) AS receita
    FROM mart_sales_summary
    GROUP BY mes
    ORDER BY receita DESC
    LIMIT 5
""").df()
print(insight_1)

print("\n" + "=" * 60)
print("INSIGHT 2: Taxa de recorrência de clientes")
print("=" * 60)
insight_2 = con.execute("""
    SELECT
        CASE WHEN total_pedidos = 1 THEN 'Única compra'
             ELSE 'Recorrente' END AS perfil,
        COUNT(*) AS clientes,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS percentual
    FROM mart_customer_segments
    GROUP BY 1
""").df()
print(insight_2)

print("\n" + "=" * 60)
print("INSIGHT 3: Top 5 categorias por receita")
print("=" * 60)
insight_3 = con.execute("""
    SELECT categoria, SUM(receita_total) AS receita, SUM(total_pedidos) AS pedidos
    FROM mart_sales_summary
    GROUP BY categoria
    ORDER BY receita DESC
    LIMIT 5
""").df()
print(insight_3)

print("\n" + "=" * 60)
print("INSIGHT 4: Satisfação média dos clientes (nota_media)")
print("=" * 60)
insight_4 = con.execute("""
    SELECT
        ROUND(nota_media) AS nota_arredondada,
        COUNT(*) AS clientes
    FROM mart_customer_segments
    GROUP BY 1
    ORDER BY 1
""").df()
print(insight_4)

print("\n" + "=" * 60)
print("INSIGHT 5: Top 5 estados por valor total gasto")
print("=" * 60)
insight_5 = con.execute("""
    SELECT estado_cliente, SUM(valor_total) AS valor_total, COUNT(*) AS clientes
    FROM mart_customer_segments
    GROUP BY estado_cliente
    ORDER BY valor_total DESC
    LIMIT 5
""").df()
print(insight_5)

con.close()