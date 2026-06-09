## Dataset

Os dados utilizados são do Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Baixe e coloque em:
data/raw/


## 📊 Insights de Negócio
Usando Python, Pandas e DuckDB, extraímos os seguintes dados da operação da Olist:
1. **Pico de Receita:** O mês com maior faturamento foi [olhe no terminal e coloque aqui].
2. **Top Categorias:** As categorias que mais trazem receita são: Beleza & Saúde, Relógios, Cama/Mesa/Banho, Esportes e Informática.
3. **Satisfação:** A grande maioria dos clientes avalia as compras com nota 5 (mais de [coloque o numero] avaliações).

## 🏗️ Arquitetura de Dados (dbt)

O pipeline de transformação foi construído utilizando **dbt Core** acoplado ao **DuckDB**, seguindo as melhores práticas de modelagem analítica. Atualmente, o projeto conta com as seguintes camadas:

* **Sources (Raw):** Dados brutos extraídos do e-commerce.
* **Staging:** Primeira camada do dbt. Responsável por limpeza de dados sujos (ex: `COALESCE`), tipagem correta de colunas (`CAST`) e padronização de nomenclatura.
* **Intermediate:** Camada de cruzamento e aplicação de regras de negócio simples, preparando o terreno para a camada analítica final.

### Grafo de Linhagem (Lineage Graph)

Abaixo está a representação visual (DAG) do fluxo de dados que compõe a nossa primeira entidade enriquecida:

```text
[ Sources ]                [ Staging ]                  [ Intermediate ]

raw_orders      -------->  stg_orders      ---\
                                               |----->  int_orders_enriched
raw_customers   -------->  stg_customers   ---/

raw_order_items -------->  stg_order_items
raw_payments    -------->  stg_payments
raw_reviews     -------->  stg_reviews
raw_products    -------->  stg_products
raw_sellers     -------->  stg_sellers