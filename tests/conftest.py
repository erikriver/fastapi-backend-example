import secrets
import string
import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from starlette.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.db import Base, Vehicle, engine, async_session_maker
from app.main import app


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="session")
async def db():
    async with async_session_maker() as session:
        yield session
        await session.rollback()
        await session.close()


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="function", autouse=True)
async def auto_rollback(db: AsyncSession):
    await db.rollback()


def generate_random_string(length: int) -> str:
    return "".join(secrets.choice(string.ascii_uppercase) for i in range(length))


@pytest_asyncio.fixture(scope="session")
def create_vehicle(db: AsyncSession):
    async def inner():
        vehicle = Vehicle(
            vin=generate_random_string(17),
            make=generate_random_string(10),
            model=generate_random_string(8),
            model_year=generate_random_string(4),
            body_class=generate_random_string(8),
        )
        db.add(vehicle)
        await db.commit()
        return vehicle

    return inner


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
