from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .model import get_async_session
from .config import get_settings
from .schemas import Vehicle
from .crud import get_vehicle, delete_vehicle
from .service import export_to_parquet

settings = get_settings()

router = APIRouter(prefix=settings.api_prefix, tags=["vehicule"])


@router.get("/lookup/{vin}", response_model=Vehicle)
async def lookup(vin: str, session: AsyncSession = Depends(get_async_session)):
    vehicle = await get_vehicle(vin, session)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.delete("/remove/{vin}")
async def remove(vin: str, session: AsyncSession = Depends(get_async_session)):
    vehicle = await delete_vehicle(vin, session)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.post("/export")
async def export():
    file_path = await export_to_parquet()
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=vehicles.parquet"},
    )
