# Databricks notebook source
# DBTITLE 1,Cell 1
import dlt
from pyspark.sql.functions import explode, round, monotonically_increasing_id

# COMMAND ----------

# DBTITLE 1,Cell 2
@dlt.table(
    name="fact_itens",
    comment="Tabela fato de itens de venda - Camada Silver"
)
def fact_itens():
    df = spark.read.table("sales_api.bronze.carts")
    
    df_itens = df.select(
        "id",
        "userId",
        explode("products").alias("produto")
    )
    
    df_itens = df_itens.select(
        df_itens["id"].alias("id_sales"),
        df_itens["userId"].alias("id_client"),
        df_itens["produto"]["id"].alias("id_product"),
        df_itens["produto"]["price"].alias("price"),
        df_itens["produto"]["quantity"].alias("quantity"),
        round(df_itens["produto"]["total"], 2).alias("total"),
        round(df_itens["produto"]["discountedTotal"], 2).alias("discountedTotal"),
        round(df_itens["produto"]["discountPercentage"], 2).alias("discountPercentage")
    ).withColumn("id", monotonically_increasing_id())
    
    return df_itens


# COMMAND ----------

