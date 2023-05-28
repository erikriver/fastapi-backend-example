from enum import Enum
from pydantic import BaseModel


class Vin(BaseModel):
    vin: str


class VehicleAPI(Vin):
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
    cached: bool

    class Config:
        orm_mode = True
