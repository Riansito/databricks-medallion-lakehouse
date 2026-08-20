# Databricks notebook source
# DBTITLE 1,Cell 1

import requests

url = "https://dummyjson.com/"
endpoints = ["carts", "users", "products?limit=0"]


# COMMAND ----------

# DBTITLE 1,Cell 2
import requests

def extract_data(endpoints):
    data = {}

    for endpoint in endpoints:

        response = requests.get(url + endpoint)
        response.raise_for_status()

        json_data = response.json()

        if endpoint == "carts":

            transformed_data = [
                {
                    "id": cart["id"],
                    "userId": cart["userId"],
                    "total": cart["total"],
                    "discountedTotal": cart["discountedTotal"],
                    "totalProducts": cart["totalProducts"],
                    "totalQuantity": cart["totalQuantity"],
                    "products": cart["products"]
                }
                for cart in json_data["carts"]
            ]

            data["carts"] = transformed_data

        elif endpoint == "users":

            transformed_data = [
                {
                    "id": user["id"],
                    "firstName": user["firstName"],
                    "lastName": user["lastName"],
                    "age": user["age"],
                    "gender": user["gender"],
                    "email": user["email"],
                    "city": user["address"]["city"],
                    "state": user["address"]["state"],
                    "country": user["address"]["country"],
                    "role": user["role"]
                }
                for user in json_data["users"]
            ]

            data["users"] = transformed_data

        elif endpoint == "products?limit=0":

            transformed_data = [
                {
                    "id": str(product.get("id")),
                    "title": product.get("title"),
                    "description": product.get("description"),
                    "category": product.get("category"),
                    "price": str(product.get("price")),
                    "discountPercentage": str(product.get("discountPercentage")),
                    "rating": str(product.get("rating")),
                    "stock": str(product.get("stock")),
                    "brand": (
                        str(product.get("brand"))
                        if product.get("brand") is not None
                        else None
                    ),
                    "sku": product.get("sku"),
                    "weight": str(product.get("weight")),
                    "availabilityStatus": product.get("availabilityStatus"),
                    "returnPolicy": product.get("returnPolicy"),
                    "minimumOrderQuantity": str(
                        product.get("minimumOrderQuantity")
                    )
                }
                for product in json_data["products"]
            ]

            data["products"] = transformed_data

    return data


def create_bronze_tables(data):

    for table_name, records in data.items():

        df = spark.createDataFrame(records)

        df.write \
            .format("delta") \
            .mode("overwrite") \
            .saveAsTable(f"sales_api.bronze.{table_name}")



# COMMAND ----------

data = extract_data(endpoints)

create_bronze_tables(data)