import pytest
from fastapi.testclient import TestClient

from project.app import app


# Inicializando o cliente de teste para os testes utilizando fixture
@pytest.fixture
def client():
    client = TestClient(app)
    return client
