import importlib
from unittest.mock import patch

from pyspark.sql.types import (
    ArrayType,
    DoubleType,
    IntegerType,
    StructField,
    StructType,
)

fact_itens = getattr(
    importlib.import_module("silver.01_silver_fact_itens"), "fact_itens"
)
fact_sales = getattr(
    importlib.import_module("silver.02_silver_fact_sales"), "fact_sales"
)


def test_fact_sales(spark):
    # Prepare dummy data for bronze carts
    data = [
        (1, 97, 2328.0, 1941.0, 5, 10),
    ]
    schema = [
        "id",
        "userId",
        "total",
        "discountedTotal",
        "totalProducts",
        "totalQuantity",
    ]
    mock_df = spark.createDataFrame(data, schema)

    from unittest.mock import PropertyMock

    with patch("pyspark.sql.SparkSession.read", new_callable=PropertyMock) as mock_read:
        mock_read.return_value.table.return_value = mock_df
        result_df = fact_sales()

        # Verify schema mapping and aliases
        assert "id_client" in result_df.columns
        row = result_df.collect()[0]
        assert row["id"] == 1
        assert row["id_client"] == 97
        assert row["total"] == 2328.0


def test_fact_itens(spark):
    schema = StructType(
        [
            StructField("id", IntegerType(), True),
            StructField("userId", IntegerType(), True),
            StructField(
                "products",
                ArrayType(
                    StructType(
                        [
                            StructField("id", IntegerType(), True),
                            StructField("price", DoubleType(), True),
                            StructField("quantity", IntegerType(), True),
                            StructField("total", DoubleType(), True),
                            StructField("discountedTotal", DoubleType(), True),
                            StructField("discountPercentage", DoubleType(), True),
                        ]
                    )
                ),
                True,
            ),
        ]
    )

    data = [
        (
            1,
            97,
            [
                {
                    "id": 59,
                    "price": 20.0,
                    "quantity": 1,
                    "total": 20.0,
                    "discountedTotal": 18.0,
                    "discountPercentage": 7.0,
                }
            ],
        )
    ]

    mock_df = spark.createDataFrame(data, schema)

    from unittest.mock import PropertyMock

    with patch("pyspark.sql.SparkSession.read", new_callable=PropertyMock) as mock_read:
        mock_read.return_value.table.return_value = mock_df
        result_df = fact_itens()

        assert "id_product" in result_df.columns
        row = result_df.collect()[0]
        assert row["id_sales"] == 1
        assert row["id_client"] == 97
        assert row["id_product"] == 59
        assert row["price"] == 20.0
