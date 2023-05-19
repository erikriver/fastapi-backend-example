import pytest


@pytest.mark.asyncio
async def test_lookup_vin_malformed(client):
    response = await client.get(f"/v1/lookup/xyz")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_lookup_vin(client, create_vehicle):
    v = await create_vehicle()
    response = await client.get(f"/v1/lookup/{v.vin}")
    assert response.status_code == 200
    assert response.json()["model"] == v.model
    assert response.json()["cached"] == True


@pytest.mark.asyncio
async def test_remove_vin_not_found(client):
    response = await client.delete(f"/v1/remove/AOEUIDRTNS1234567")
    assert response.status_code == 404
    assert response.json()["detail"] == "Vehicle doesn't exist"


@pytest.mark.asyncio
async def test_remove_vin(client, create_vehicle):
    v = await create_vehicle()
    response = await client.delete(f"/v1/remove/{v.vin}")
    assert response.status_code == 200
    assert response.json()["detail"] == f"The Vehicle {v.vin} was deleted successful."
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
