import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from models.base_model import Base

DATABASE = os.getenv('DATABASE', "sqlite+aiosqlite:///database/database.db")

engine = create_async_engine(DATABASE)
session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def create_tables(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
