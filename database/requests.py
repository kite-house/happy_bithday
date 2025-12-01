from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select, Sequence
from database.models import Base, User, Birthday
from datetime import datetime
from dotenv import get_key

engine = create_async_engine(url = get_key('.env', 'DATABASE'))
async_session = async_sessionmaker(engine)


async def async_main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def set_user(telegram_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == telegram_id))

        if not user:
            session.add(User(id = telegram_id))
            await session.commit()

async def set_birthday(telegram_id: int, name: str, date_birth: datetime) -> None:
    async with async_session() as session:
        birthday = await session.scalar(select(Birthday).where(Birthday.owner_id == telegram_id, Birthday.name == name))

        if birthday:
            raise ValueError

        session.add(Birthday(
            owner_id = telegram_id,
            name = name,
            date_birth = date_birth
        ))

        await session.commit()

async def del_birthday(telegram_id: int, name: str) -> None:
    async with async_session() as session:
        birthday = await session.execute(select(Birthday).where(Birthday.owner_id == telegram_id, Birthday.name == name))
        await session.delete(birthday.scalars().first())
        await session.commit()

    
async def get_birthdays(telegram_id: int) -> Sequence[Birthday]:
    async with async_session() as session:
        birthdays = await session.execute(select(Birthday).where(Birthday.owner_id == telegram_id))
        return birthdays.scalars().all()