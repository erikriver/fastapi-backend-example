import pytest
from app.crud import *
from app.exceptions import VehicleDeletedException


@pytest.mark.asyncio
async def test_get_vehicle(db, create_vehicle):
    v = await create_vehicle()
    result = await get_vehicle(v.vin, db)
    assert result.vin == v.vin
    assert result.model == v.model
    assert result.model_year == v.model_year
    assert result.deleted == False


@pytest.mark.asyncio
async def test_delete_vehicle(db, create_vehicle):
    v = await create_vehicle()
    result = await delete_vehicle(v.vin, db)
    assert result.vin == v.vin
    assert result.deleted == True

    with pytest.raises(VehicleDeletedException):
        result = await get_vehicle(v.vin, db)
