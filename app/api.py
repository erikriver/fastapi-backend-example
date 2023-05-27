from fastapi import Depends, APIRouter, HTTPException, Path, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from config import get_settings
from models import Vehicle as VehicleSchema
from crud import get_vehicle, delete_vehicle
from service import export_to_parquet
from exceptions import *

settings = get_settings()

router = APIRouter(prefix=settings.api_prefix, tags=["vehicule"])


@router.get("/lookup/{vin}", response_model=VehicleSchema)
async def lookup(
    vin: str = Path(min_length=17, max_length=17),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        vehicle = await get_vehicle(vin, session)
    except VehicleDeletedException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle deleted"
        )
    except VehicleNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found in vPIC"
        )
    except VPICAPIException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is an error in vPIC API",
        )
    else:
        return vehicle


@router.delete("/remove/{vin}")
async def remove(
    vin: str = Path(min_length=17, max_length=17),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        vehicle = await delete_vehicle(vin, session)
    except VehicleDeletedException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle soft deleted"
        )
    except VehicleNotCachedException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle doesn't exist"
        )
    else:
        return {
            "detail": f"The Vehicle {vehicle.vin} was deleted successful.",
            "deleted": True,
        }


@router.post("/export")
async def export():
    file_path = await export_to_parquet()
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=vehicles.parquet"},
    )
