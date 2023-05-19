from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select

from .db import get_async_session, Vehicle
from .service import get_vehicle_data
from .config import get_settings
from .exceptions import VehicleDeletedException, VehicleNotCachedException

settings = get_settings()


async def get_vehicle(vin: str, session: AsyncSession):
    result = await session.execute(select(Vehicle).where(Vehicle.vin == vin))

    try:
        vehicle = result.scalars().first()

        if vehicle.deleted == False:
            vehicle.cached = True
            return vehicle
        else:
            raise VehicleDeletedException

    except AttributeError:
        data = await get_vehicle_data(vin)
        vehicle = Vehicle(**data)
        vehicle.vin = vin
        session.add(vehicle)
        await session.commit()
        vehicle.cached = False
        return vehicle


async def delete_vehicle(vin: str, session: AsyncSession):
    try:
        result = await session.execute(select(Vehicle).where(Vehicle.vin == vin))
        vehicle = result.scalars().first()

        if vehicle.deleted == True:
            raise VehicleDeletedException

        vehicle.deleted = True
        session.add(vehicle)
        await session.commit()
        return vehicle
    except AttributeError:
        raise VehicleNotCachedException
