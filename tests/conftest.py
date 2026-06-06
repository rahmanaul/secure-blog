import pytest
from django.test import Client


@pytest.fixture
def client():
    """A Django test client for making requests."""
    return Client()
