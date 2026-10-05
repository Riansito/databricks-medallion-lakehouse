import requests_mock

from bronze.ingest_api_bronze import extract_data


def test_extract_data_carts():
    with requests_mock.Mocker() as m:
        # Mock da chamada /carts
        m.get(
            "https://dummyjson.com/carts",
            json={
                "carts": [
                    {
                        "id": 1,
                        "userId": 97,
                        "total": 2328,
                        "discountedTotal": 1941,
                        "totalProducts": 5,
                        "totalQuantity": 10,
                        "products": [
                            {
                                "id": 59,
                                "title": "Product 1",
                                "price": 20,
                                "quantity": 1,
                                "total": 20,
                                "discountPercentage": 7,
                                "discountedTotal": 18,
                            }
                        ],
                    }
                ]
            },
        )

        # Testando só o endpoint de carts para simplificar o teste unitário isolado
        data = extract_data(["carts"])

        assert "carts" in data
        assert len(data["carts"]) == 1
        assert data["carts"][0]["id"] == 1
        assert data["carts"][0]["userId"] == 97
        assert data["carts"][0]["total"] == 2328
        assert data["carts"][0]["products"][0]["title"] == "Product 1"
