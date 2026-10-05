
import importlib

vw_sales_details = getattr(
    importlib.import_module("gold.01_gold_vw_sales_details"), "vw_sales_details"
)


def test_vw_sales_details(spark):
    fact_sales = spark.createDataFrame([(1, 97)], ["id", "id_client"])

    fact_items_sales = spark.createDataFrame(
        [(1, 97, 59, 20.0, 1, 20.0, 18.0)],
        [
            "id_sales",
            "id_client",
            "id_product",
            "price",
            "quantity",
            "total",
            "discountedTotal",
        ],
    )

    dim_users = spark.createDataFrame(
        [(97, "John", "Doe", 30, "M", "New York", "NY", "USA")],
        ["id", "firstName", "lastName", "age", "gender", "city", "state", "country"],
    )

    dim_products = spark.createDataFrame(
        [(59, "Product 1", "Category A", "Brand Z", 4.5, 20.0)],
        ["id", "title", "category", "brand", "rating", "price"],
    )

    result_df = vw_sales_details(fact_sales, fact_items_sales, dim_users, dim_products)

    row = result_df.collect()[0]

    assert row["id_sale"] == 1
    assert row["client_name"] == "John Doe"
    assert row["product_name"] == "Product 1"
    assert row["quantity"] == 1
    assert row["item_total"] == 20.0
