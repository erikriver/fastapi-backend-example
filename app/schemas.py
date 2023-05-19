from enum import Enum
from pydantic import BaseModel


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
