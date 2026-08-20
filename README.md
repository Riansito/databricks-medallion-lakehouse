# 📰 E-Commerce Sales Lakehouse Analytics & Medallion Architecture

> Pipeline completo de Engenharia de Dados para extração, limpeza, modelagem dimensional e consolidação analítica de vendas de e-commerce utilizando a Arquitetura Medallion no Databricks (Delta Lake, PySpark, DLT e Workflows).

---

# 📖 Introdução

Atualmente, milhares de transações e interações de clientes são geradas continuamente por plataformas de e-commerce, tornando essencial centralizar, padronizar e disponibilizar esses dados para inteligência de negócios e tomada de decisão.

A grande maioria das APIs de e-commerce retorna respostas em documentos JSON complexos e aninhados (com listas de produtos dentro de carrinhos, objetos de localização em usuários, etc.), o que dificulta o consumo direto por dashboards ou consultas analíticas performáticas.

Este projeto resolve esse problema construindo uma arquitetura moderna de **Data Lakehouse** no Databricks. O fluxo transforma dados brutos de chamadas de API em um Lakehouse organizado sob a **Arquitetura Medallion (Bronze, Silver e Gold)**, garantindo integridade ACID, escalabilidade e visões analíticas otimizadas para BI.

---

# 🎯 Problema de Negócio

APIs de plataformas de e-commerce (como a DummyJSON) fornecem informações detalhadas de vendas, usuários e produtos, porém em formatos estruturados hierarquicamente (JSON aninhado).

Esse formato apresenta diversos desafios em ambientes de produção:

* Objetos e arrays aninhados (ex: array de produtos dentro de cada carrinho)
* Falta de padronização nos tipos de dados
* Baixa performance para consultas analíticas diretas em dados brutos
* Dificuldade de cruzamento relacional entre entidades (Fatos e Dimensões)
* Risco de ineficiência no processamento de cargas diárias
* Dificuldade de integração direta com ferramentas de BI sem pré-processamento

O objetivo deste projeto é estruturar um pipeline automatizado que ingere, limpa, desaninha e modela esses dados em um modelo analítico consolidado e performático.

---

# 🚀 Objetivos

O projeto foi desenvolvido para demonstrar um pipeline end-to-end de Engenharia de Dados utilizando as melhores práticas do ecossistema Databricks e Delta Lake.

Entre os principais objetivos estão:

* Automatizar a ingestão de dados de vendas, clientes e produtos via API REST
* Armazenar o dado bruto em formato Delta Lake na camada Bronze
* Construir a camada Silver aplicando limpeza, tipagem e desaninamento (`explode`) via PySpark e Delta Live Tables (DLT)
* Modelar um esquema dimensional completo (Fatos e Dimensões)
* Consolidar os dados na camada Gold através de visões prontas para inteligência de negócio
* Orquestrar todas as etapas de forma dependente e automática via Databricks Workflows (Jobs)

---

# 🏗 Arquitetura

```text
                 API REST (DummyJSON)
                          │
                          ▼
              Python Ingestion (Requests)
                          │
                          ▼
            sales_api.bronze (Delta Lake)
                          │
                          ▼
              Databricks Workflows (Job)
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
   Delta Live Tables (DLT)      PySpark Processing
             │                         │
             ▼                         ▼
   sales_api.silver           sales_api.silver
    (fact_itens)          (fact_sales, dim_users...)
             │                         │
             └────────────┬────────────┘
                          │
                          ▼
              sales_api.gold (vw_sales_details)
                          │
                          ▼
              Consumo BI / Analytics

```
## Ilustração da Arquitetura
<img width="1672" height="941" alt="ChatGPT Image 20 de ago  de 2026, 12_11_48" src="https://github.com/user-attachments/assets/c2023e2b-9a6c-4173-84fd-885297bb2e21" />

---

# ⚙ Tecnologias Utilizadas

### Linguagens

* Python
* PySpark
* SQL

### Plataforma & Lakehouse

* Databricks
* Delta Lake
* Unity Catalog

### Processamento & Orquestração

* Delta Live Tables (DLT)
* Databricks Workflows (Jobs)

### Bibliotecas Python

* Requests
* PySpark SQL (`functions`, `types`)

---

# 📂 Estrutura do Projeto

```text
databricks-sales-lakehouse/
│
├── README.md
│
└── src/
    ├── bronze/
    │   └── 01_ingest_api_bronze.py
    │
    ├── silver/
    │   ├── 01_silver_fact_itens.py
    │   ├── 02_silver_fact_sales.py
    │   ├── 03_silver_dim_users.py
    │   └── 04_silver_dim_products.py
    │
    └── gold/
        └── 01_gold_vw_sales_details.py

```

---

# 📊 Modelagem Lakehouse (Medallion)

O projeto é estruturado seguindo as 3 camadas da Arquitetura Medallion em formato Delta:

## Camada Bronze (Raw)

Tabelas com os dados brutos exatamente como recebidos da API:

* `sales_api.bronze.carts`
* `sales_api.bronze.users`
* `sales_api.bronze.products`

## Camada Silver (Trusted)

Tabelas tratadas, deduplicadas e organizadas em modelo dimensional:

* **Fatos:**
* `sales_api.silver.fact_sales`
* `sales_api.silver.fact_itens`


* **Dimensões:**
* `sales_api.silver.dim_users`
* `sales_api.silver.dim_products`



## Camada Gold (Refined)

View analítica consolidada para consumo de negócios:

* `sales_api.gold.vw_sales_details`

---

# 🔄 Pipeline

## 1. Ingestão (Bronze)

Um script Python consome os endpoints da API (`/carts`, `/users`, `/products`).

Os registros recuperados são convertidos em DataFrames e salvos como tabelas Delta na camada `sales_api.bronze` utilizando modo de sobregravação controlada e gerenciamento de schema (`overwriteSchema`).

Nenhuma transformação de regra de negócio é feita nesta etapa.

---

## 2. Limpeza e Modelagem (Silver)

O processamento da camada Silver realiza:

* desaninamento de arrays de produtos via função `explode()`
* seleção e padronização dos atributos de clientes, produtos e vendas
* conversão e arredondamento de tipos numéricos (preço, descontos, métricas)
* geração de chaves primárias/surrogadas com `monotonically_increasing_id()`
* declaração e execução via PySpark e **Delta Live Tables (DLT)**

O processamento da camada Silver é executado via **Delta Live Tables (DLT)** e PySpark para desaninhar arrays, aplicar regras de negócio, limpar schemas e construir as tabelas Fato e Dimensão.

<img width="1654" height="836" alt="Captura de tela 2026-08-20 122646" src="https://github.com/user-attachments/assets/343edde1-3416-40b5-bb12-dc4cbc034790" />

---

## 3. Consolidação Analítica (Gold)

A camada Gold combina as tabelas fato e dimensão em uma única visão denormalizada otimizada para performance analítica.

A view `sales_api.gold.vw_sales_details` realiza o cruzamento de:

* dados da transação/venda
* atributos demográficos do cliente (nome completo, idade, gênero, cidade, estado, país)
* atributos detalhados do produto (nome, categoria, marca, avaliação)
* métricas financeiras por item (preço unitário, quantidade, total e total com desconto)

---

# ⚙ Orquestração com Databricks Workflows

O pipeline completo é gerenciado por um Job no **Databricks Workflows** com 3 tarefas encadeadas e dependentes:

1. **Task 1 (Bronze Ingestion):** Executa o notebook de consumo da API em Python e grava os dados brutos Delta.
2. **Task 2 (Silver DLT Pipeline):** Dispara a atualização declarativa do pipeline Delta Live Tables para atualização das tabelas Silver. *(Depende da Task 1)*
3. **Task 3 (Gold Consolidation):** Executa o notebook PySpark para consolidar os joins e publicar a view Gold no Unity Catalog. *(Depende da Task 2)*

<img width="1627" height="837" alt="Captura de tela 2026-08-20 122602" src="https://github.com/user-attachments/assets/b8c73b5a-7570-4185-95a2-1feb4c42f611" />

---

# ▶ Como executar

## 1. Configurar o Catálogo e Schemas no Databricks

No Databricks SQL Editor ou em uma célula de notebook, execute:

```sql
CREATE CATALOG IF NOT EXISTS sales_api;
CREATE SCHEMA IF NOT EXISTS sales_api.bronze;
CREATE SCHEMA IF NOT EXISTS sales_api.silver;
CREATE SCHEMA IF NOT EXISTS sales_api.gold;

```

## 2. Importar o Código

* Importe os scripts da pasta `src/` para o seu Workspace do Databricks.

## 3. Configurar o Workflow (Job)

1. Vá em **Workflows** $\rightarrow$ **Create Job**.
2. Crie as 3 tarefas encadeadas conforme a estrutura descrita na seção de Orquestração.
3. Clique em **Run Now** para disparar o pipeline completo de ponta a ponta.

---

# 📈 Melhorias Futuras

* Implementação de carga incremental (SCD Type 2) para a dimensão de clientes na Silver
* Adição de suporte a alertas e notificações em caso de falhas na execução do Job
* Automação de testes de qualidade de dados com regras de expectativa (*Expectations*) do Delta Live Tables
* Integração contínua e deploy dos notebooks via Databricks Asset Bundles (DABs) e GitHub Actions
* Conexão da camada Gold com painéis do Power BI via DirectQuery / Databricks SQL Warehouse

---

# 👨‍💻 Autor

**Rian Freires Da Costa Silva**

