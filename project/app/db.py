import os
from asyncio import sleep, current_task

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker

from .config import settings


engine = create_async_engine(settings.database_url, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def async_get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async_session_factory = sessionmaker(engine, class_=AsyncSession)
AsyncSession = async_scoped_session(async_session_factory, scopefunc=current_task)

async_session = AsyncSession()