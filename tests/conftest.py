from typing import Type

from django.contrib.auth import get_user_model

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from estate_api.models import Transaction
from tests.factories import TransactionFactory

register(TransactionFactory)


@pytest.fixture
def api_client() -> APIClient:
    """Return an authorized APIClient object."""
    test_user = get_user_model().objects.create_user(
        username="foo", password="bar"
    )
    token = Token.objects.create(user=test_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.fixture
def transaction_fixture(
    transaction_factory: Type[TransactionFactory],
) -> Transaction:
    return transaction_factory()
