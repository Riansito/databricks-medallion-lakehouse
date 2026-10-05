import sys
from unittest.mock import MagicMock

import pytest

# Create a mock for dlt so imports don't fail
mock_dlt = MagicMock()


# Mock dlt.table decorator so it just returns the function
def mock_dlt_table(*args, **kwargs):
    def decorator(func):
        return func

    return decorator


mock_dlt.table = mock_dlt_table
sys.modules["dlt"] = mock_dlt

from pyspark.sql import SparkSession  # noqa: E402


@pytest.fixture(scope="session")
def spark():
    """
    Creates a SparkSession for testing purposes.
    """
    spark = (
        SparkSession.builder.appName("pytest-pyspark-local-testing")
        .master("local[1]")
        .getOrCreate()
    )

    # Inject spark into builtins to mock Databricks environment
    import builtins

    builtins.spark = spark

    yield spark
    spark.stop()
