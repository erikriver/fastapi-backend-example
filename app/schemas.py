from enum import Enum
from pydantic import BaseModel


# Filed constants from vPIC API
class VehicleAPIConstant(int, Enum):
    MAKE_FIELD_ID = 26
    MODEL_FILED_ID = 28
    MODEL_YEAR_FILED_ID = 29
    BODY_CLASS_FIELD_ID = 5


class Vin(BaseModel):
    vin: str


class VehicleCreate(Vin):
    make: str
    model: str
    model_year: str
    body_class: str


class VehicleDelete(Vin):
    deleted: bool


class Vehicle(Vin):
    make: str
    model: str
    model_year: str
    body_class: str

    class Config:
        orm_mode = True
