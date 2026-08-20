# Databricks notebook source
# DBTITLE 1,Cell 1
from pyspark.sql.functions import col, concat, lit

# 1. Carregar tabelas da Silver geradas pelo DLT
fact_sales = spark.read.table("sales_api.silver.fact_sales")
fact_items_sales = spark.read.table("sales_api.silver.fact_itens")
dim_users = spark.read.table("sales_api.silver.dim_users")
dim_products = spark.read.table("sales_api.silver.dim_products")

def vw_sales_details(fact_sales, fact_items_sales, dim_users, dim_products):
    return (
        fact_items_sales
        .join(fact_sales, fact_items_sales.id_sales == fact_sales.id, "inner")
        .join(dim_users, fact_sales.id_client == dim_users.id, "inner")
        .join(dim_products, fact_items_sales.id_product == dim_products.id, "inner")
        .select(
            fact_sales.id.alias("id_sale"),
            fact_sales.id_client,
            concat(dim_users.firstName, lit(" "), dim_users.lastName).alias("client_name"),
            dim_users.age.alias("client_age"),
            dim_users.gender.alias("client_gender"),
            dim_users.city.alias("client_city"),
            dim_users.state.alias("client_state"),
            dim_users.country.alias("client_country"),
            fact_items_sales.id_product,
            dim_products.title.alias("product_name"),
            dim_products.category.alias("product_category"),
            dim_products.brand.alias("product_brand"),
            dim_products.rating.alias("product_rating"),
            dim_products.price.cast("double").alias("unit_price"),
            fact_items_sales.quantity.cast("int").alias("quantity"),
            fact_items_sales.total.cast("double").alias("item_total"),
            fact_items_sales.discountedTotal.cast("double").alias("item_discounted_total")
        )
    )

# 2. Executar e Salvar na Gold
df_gold = vw_sales_details(fact_sales, fact_items_sales, dim_users, dim_products)

df_gold.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("sales_api.gold.vw_sales_details")


# COMMAND ----------

display(df_gold)