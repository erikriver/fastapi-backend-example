from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select

from .model import get_async_session, Vehicle
from .service import get_vehicle_data


async def get_vehicle(vin: str, session: AsyncSession):
    result = await session.execute(select(Vehicle).filter_by(vin=vin))
    try:
        vehicle = result.fetchone()[0]
        print(vehicle)
        if vehicle.deleted == False:
            return vehicle
    except TypeError:
        data = get_vehicle_data(vin)
        vehicle = Vehicle(**data)
        vehicle.vin = vin
        session.add(vehicle)
        await session.commit()
        return vehicle


async def delete_vehicle(vin: str, session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(
            select(Vehicle).filter_by(vin=vin, deleted=False).limit(1)
        )
        vehicle = result.fetchone()[0]
        vehicle.deleted = True
        session.add(vehicle)
        await session.commit()
        return vehicle
    except TypeError:
        pass
