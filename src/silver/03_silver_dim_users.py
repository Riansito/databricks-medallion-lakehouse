# Databricks notebook source
# DBTITLE 1,Cell 1

import os
import dlt

CATALOG_NAME = os.getenv("CATALOG_NAME", "sales_api")

@dlt.table(name="dim_users", comment="Tabela dimensão de usuarios - Camada Silver")
def dim_users():
    return spark.read.table(f"{CATALOG_NAME}.bronze.users")
