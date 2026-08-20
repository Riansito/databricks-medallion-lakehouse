# Databricks notebook source
# DBTITLE 1,Cell 1

import dlt

@dlt.table(
    name="dim_users",
    comment="Tabela dimensão de usuarios - Camada Silver"
)
def dim_users():
    return spark.read.table("sales_api.bronze.users")