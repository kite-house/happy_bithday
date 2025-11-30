from aiogram import Bot, Dispatcher
from dotenv import get_key
from database.requests import async_main
from src.handlers import router
import asyncio
import logging


async def main():
    await async_main()

    bot = Bot(token=get_key('.env', 'TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    logging.info('System: start')

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('System: stop')
    