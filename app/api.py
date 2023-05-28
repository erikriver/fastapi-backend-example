from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException, Path, Header, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.config import get_settings
from app.models import Vehicle as VehicleSchema
from app.crud import get_vehicle, delete_vehicle
from app.service import export_to_parquet
from app.security import verify_token, create_access_token
from app.exceptions import *

settings = get_settings()

router = APIRouter(prefix=settings.api_prefix, tags=["vehicule"])
security = APIRouter(prefix="/secutiry", tags=["security"])


@router.get("/lookup/{vin}", response_model=VehicleSchema)
async def lookup(
    vin: str = Path(min_length=17, max_length=17),
    token: Annotated[str, Header()] = None,
    session: AsyncSession = Depends(get_async_session),
):
    if not token or not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    try:
        vehicle = await get_vehicle(vin, session)
    except VehicleDeletedException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle deleted")
    except VehicleNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found in vPIC")
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
    token: Annotated[str, Header()] = None,
    session: AsyncSession = Depends(get_async_session),
):
    if not token or not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    try:
        vehicle = await delete_vehicle(vin, session)
    except VehicleDeletedException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle soft deleted")
    except VehicleNotCachedException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle doesn't exist")
    else:
        return {
            "detail": f"The Vehicle {vehicle.vin} was deleted successful.",
            "deleted": True,
        }


@router.post("/export")
async def export(
    token: Annotated[str, Header()],
):
    if not token or not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    file_path = await export_to_parquet()
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=vehicles.parquet"},
    )


@security.post("/generate_token")
def generate_token():
    """Generate JWT token endpoint

    Returns:
        json: jwt token
    """
    access_token = create_access_token()
    return {"access_token": access_token}
