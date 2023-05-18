from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from .model import get_async_session
from .config import get_settings
from .schemas import Vehicle
from .crud import get_vehicle, delete_vehicle

settings = get_settings()

router = APIRouter(prefix=settings.api_prefix, tags=["vehicule"])


@router.get("/lookup/{vin}", response_model=Vehicle)
async def lookup(vin: str, session: AsyncSession = Depends(get_async_session)):
    vehicle = await get_vehicle(vin, session)
    return vehicle


@router.delete("/remove/{vin}")
async def remove(vin: str, session: AsyncSession = Depends(get_async_session)):
    vehicle = await delete_vehicle(vin, session)
    return vehicle


@router.post("/export")
async def export():
    data = "data"
    return {"message": f"Export {data}!"}
