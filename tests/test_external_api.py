import json
from pathlib import Path
import pytest
import pytest_asyncio

from app.service import get_vehicle_raw_data, get_vehicle_data
from app.exceptions import VPICAPIException, VehicleNotFoundException
from app.models import VehicleAPI


VPIC_API = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/1XP5DB9X7YN526158?format=json"


@pytest_asyncio.fixture
async def json_mock():
    "API response mocked from a JSON file previously saved"
    p = Path(__file__).with_name("vpic-api.json")
    data = {}
    # Opening JSON file
    with p.open("r") as f:
        data = json.load(f)
    yield data


async def test_get_vehicle_raw_data(requests_mock, json_mock):
    "Testing the response in raw data"
    requests_mock.get(VPIC_API, json=json_mock, status_code=200)

    response = await get_vehicle_raw_data("1XP5DB9X7YN526158")
    assert len(response) == 4
    assert "Results" in response
    assert response["Count"] == 136


async def test_get_vehicle_raw_data_error(requests_mock, json_mock):
    "Testing an error in the external API"
    requests_mock.get(VPIC_API, json=json_mock, status_code=500)

    with pytest.raises(VPICAPIException):
        response = await get_vehicle_raw_data("1XP5DB9X7YN526158")


async def test_get_vehicle_data(requests_mock, json_mock):
    "Testing the response with the data cleaned"
    requests_mock.get(VPIC_API, json=json_mock, status_code=200)

    vehicle = await get_vehicle_data("1XP5DB9X7YN526158")
    assert type(vehicle) == VehicleAPI
    assert len(vehicle.dict()) == 5
    assert vehicle.vin == "1XP5DB9X7YN526158"
    assert vehicle.make == "VOLVO TRUCK"
    assert vehicle.model == "VNL"
    assert vehicle.model_year == "2014"
    assert vehicle.body_class == "Truck-Tractor"
