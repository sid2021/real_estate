from typing import Dict, List, Union
import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from estate_api.taxonomies import INVALID_PARAMS_MSG

COMMON_INVALID_HTTP_METHODS = ["get", "put", "patch", "delete"]
ERROR_MSG = (
    f"{INVALID_PARAMS_MSG} Please specify outward"
    " postal code (area and district)."
)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url, payload,status,expected_response",
    [
        (
            reverse("transaction-prices"),
            {"location": "L1", "from": "1999-01", "to": "1999-12"},
            status.HTTP_200_OK,
            {"L1": {}},
        ),
        (
            reverse("transaction-prices"),
            {},
            status.HTTP_400_BAD_REQUEST,
            [ERROR_MSG],
        ),
        (
            reverse("transaction-prices"),
            {"location": "L1", "from": "1999-01", "to": "1999-12"},
            status.HTTP_200_OK,
            {"L1": {}},
        ),
        (
            reverse("transaction-prices"),
            {},
            status.HTTP_400_BAD_REQUEST,
            [ERROR_MSG],
        ),
    ],
)
def test_transaction_endpoints_return_expected_status_and_data(
    api_client: APIClient,
    url: str,
    payload: Dict,
    status: status,
    expected_response: Union[Dict, List],
):
    """Assert that the POST request to the /transactions/prices/ endpoint
    returns expected data and status.
    """
    response = api_client.post(url, data=payload)
    assert response.status_code == status
    assert response.json() == expected_response


@pytest.mark.django_db
@pytest.mark.parametrize("method", COMMON_INVALID_HTTP_METHODS)
def test_transaction_endpoints_return_405_with_invalid_methods(
    api_client: APIClient, method: str
):
    """Assert that the request != POST to the /transactions/prices/ endpoint
    returns HTTP 405 status code.
    """
    http_method = getattr(api_client, method)

    url = reverse("transaction-prices")
    response = http_method(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    url = reverse("transaction-numbers")
    response = http_method(url)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
