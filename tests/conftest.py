import pytest
from rest_framework.test import APIClient

from testapp import urls  # noqa


@pytest.fixture
def api_client():
    client = APIClient()
    return client
