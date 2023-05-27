import pytest


@pytest.mark.asyncio
async def test_lookup_vin_malformed(client):
    # Less than 17 chars
    response = await client.get(f"/v1/lookup/XYZ123")
    assert response.status_code == 422

    # More than 17 chars
    response = await client.get(f"/v1/lookup/AOEUIDRTNS12345678")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_lookup_vin(client, vehicle):
    response = await client.get(f"/v1/lookup/{vehicle.vin}")
    assert response.status_code == 200
    assert response.json()["make"] == vehicle.make
    assert response.json()["model"] == vehicle.model
    assert response.json()["model_year"] == vehicle.model_year
    assert response.json()["body_class"] == vehicle.body_class
    assert response.json()["cached"] == True


@pytest.mark.asyncio
async def test_remove_vin_not_found(client):
    response = await client.delete(f"/v1/remove/AOEUIDRTNS1234567")
    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle doesn't exist"


@pytest.mark.asyncio
async def test_remove_vin(client, vehicle):
    response = await client.delete(f"/v1/remove/{vehicle.vin}")
    assert response.status_code == 200
    assert (
        response.json()["detail"]
        == f"The Vehicle {vehicle.vin} was deleted successful."
    )
    assert response.json()["deleted"] == True


@pytest.mark.asyncio
async def test_export_vins(client, db):
    response = await client.post(f"/v1/export")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert (
        response.headers["content-disposition"]
        == "attachment; filename=vehicles.parquet"
    )
