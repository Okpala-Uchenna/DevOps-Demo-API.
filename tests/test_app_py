import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.get_json()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_add_item(client):
    response = client.post("/items", json={"name": "Ansible"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "Ansible"


def test_add_item_missing_name(client):
    response = client.post("/items", json={})
    assert response.status_code == 400
