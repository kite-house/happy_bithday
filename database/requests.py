from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from database.models import Base, User, Birthday
from sqlalchemy import select
from dotenv import get_key
import asyncio


engine = create_async_engine(url = get_key('.env', 'DATABASE'))
async_session = async_sessionmaker(engine)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def set_user(telegram_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == telegram_id))

        if not user:
            session.add(User(id = telegram_id))
            await session.commit()


