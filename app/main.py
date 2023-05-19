from typing_extensions import Annotated

from fastapi import Depends, FastAPI

from app.db import create_db_and_tables
from app.api import router as api_router
from app.config import Settings, get_settings


def get_application(settings: Settings) -> FastAPI:
    application = FastAPI(title=settings.project_name, debug=settings.debug)
    application.include_router(api_router)
    return application


app = get_application(get_settings())


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
