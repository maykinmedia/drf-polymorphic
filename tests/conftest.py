import pytest
from rest_framework.test import APIClient

from testapp import urls  # noqa


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture()
def no_warnings(capsys):
    """make sure test emits no warnings"""
    yield capsys
    captured = capsys.readouterr()
    assert not captured.out
    assert not captured.err
