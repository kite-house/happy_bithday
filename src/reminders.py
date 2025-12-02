from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import requests
from aiogram import Bot
from dotenv import get_key
import datetime

bot = Bot(token=get_key('.env', 'TOKEN'))
scheduler = AsyncIOScheduler()

async def check_birthdays():
    today = datetime.date.today()
    data = await requests.get_all_birthdays()
    notify = []

    for line in data:
        birthday_this_year = line.date_birth.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = line.date_birth.replace(year=today.year + 1)

        delta = (birthday_this_year - today).days
        
        if delta == 3:
            notify.append(line)

    for line in notify:
        await bot.send_message(line.owner_id, f'У вашего друга {line.name} день рождения через 3 дня!')


scheduler.add_job(check_birthdays, 'interval', days = 1)