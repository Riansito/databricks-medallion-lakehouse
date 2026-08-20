# Databricks notebook source
# DBTITLE 1,Cell 1
import dlt

# COMMAND ----------

# DBTITLE 1,Cell 2

@dlt.table(
    name="dim_products",
    comment="Tabela dimensão de produtos  - Camada Silver"
)
def dim_products():
    df = spark.read.table("sales_api.bronze.products")
    
    
    return df.select(
        df.id.cast("int"),
        df.title,
        df.category,
        df.price.cast("double"),
        df.discountPercentage.cast("double"),
        df.stock.cast("int"),
        df.rating.cast("double"),
        df.description,
        df.weight.cast("int"),
        df.returnPolicy,
        df.availabilityStatus,
        df.brand,
        df.sku,
        df.minimumOrderQuantity.cast("int")
    )

# COMMAND ----------

# DBTITLE 1,Cell 3
