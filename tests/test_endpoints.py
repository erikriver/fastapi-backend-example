import pytest
from unittest.mock import patch


@pytest.mark.asyncio
@patch("app.api.verify_token", return_value=True)
async def test_lookup_vin_malformed(verify_token_mock, client):
    # Less than 17 chars
    response = await client.get(f"/v1/lookup/XYZ123", headers={"token": "test-token"})
    assert response.status_code == 422

    # More than 17 chars
    response = await client.get(
        f"/v1/lookup/AOEUIDRTNS12345678",
        headers={"token": "test-token"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
@patch("app.api.verify_token", return_value=True)
async def test_lookup_vin(verify_token_mock, client, vehicle):
    response = await client.get(
        f"/v1/lookup/{vehicle.vin}",
        headers={"token": "test-token"},
    )
    assert response.status_code == 200
    assert response.json()["make"] == vehicle.make
    assert response.json()["model"] == vehicle.model
    assert response.json()["model_year"] == vehicle.model_year
    assert response.json()["body_class"] == vehicle.body_class
    assert response.json()["cached"] == True


@pytest.mark.asyncio
@patch("app.api.verify_token", return_value=True)
async def test_remove_vin_not_found(verify_token_mock, client):
    response = await client.delete(
        f"/v1/remove/AOEUIDRTNS1234567",
        headers={"token": "test-token"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle doesn't exist"


@pytest.mark.asyncio
@patch("app.api.verify_token", return_value=True)
async def test_remove_vin(verify_token_mock, client, vehicle):
    response = await client.delete(
        f"/v1/remove/{vehicle.vin}",
        headers={"token": "test-token"},
    )
    assert response.status_code == 200
    assert response.json()["detail"] == f"The Vehicle {vehicle.vin} was deleted successful."
    assert response.json()["deleted"] == True


@pytest.mark.asyncio
@patch("app.api.verify_token", return_value=True)
async def test_export_vins(verify_token_mock, client, db):
    response = await client.post(
        f"/v1/export",
        headers={"token": "test-token"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.headers["content-disposition"] == "attachment; filename=vehicles.parquet"
