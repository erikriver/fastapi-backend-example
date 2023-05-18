import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_lookup_vin():
    vin = "xyz"
    response = client.get(f"/v1/lookup/{vin}")
    assert response.status_code == 200
    assert response.json() == {"vin": vin}


def test_remove_vin():
    vin = "xyz"
    response = client.delete(f"/v1/remove/{vin}")
    assert response.status_code == 200
    assert response.json() == {"vin": f"{vin} deleted"}


def test_export_vins():
    response = client.post(f"/v1/export")
    assert response.status_code == 200
    assert response.json() == {"message": f"Export data!"}
