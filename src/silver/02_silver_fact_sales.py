# Databricks notebook source
# DBTITLE 1,Cell 1
import dlt

# COMMAND ----------

# DBTITLE 1,Cell 2
@dlt.table(
    name="fact_sales",
    comment="Tabela fato de vendas - Camada Silver"
)
def fact_sales():
    df = spark.read.table("sales_api.bronze.carts")
    
    return df.select(
        "id",
        df["userId"].alias("id_client"),
        "total",
        "discountedTotal",
        "totalProducts",
        "totalQuantity"
    )

# COMMAND ----------

