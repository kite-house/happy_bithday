from aiogram import F, Router, types
from aiogram.filters.command import Command
from database import requests
from datetime import datetime
router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await requests.set_user(message.from_user.id)
    await message.reply("Hello world!")

@router.message(Command('add'))
async def add(message: types.Message):
    try:
        name, date = message.text.split()[1:3]
        date = datetime.strptime(date, "%d.%m.%Y").date()
        await requests.set_birthday(message.from_user.id, name, date)
    except ValueError as error:
        return await message.reply(str(error))
    await message.reply('Успешно добавил!')

@router.message(Command('del'))
async def add(message: types.Message):
    name = message.text.split()[1]
    await requests.del_birthday(message.from_user.id, name)
    await message.reply('Успешно удален!')

@router.message(Command('get'))
async def add(message: types.Message):
    data = await requests.get_birthdays(message.from_user.id)
    if not data:
        return await message.reply("Вы не добавили ещё ни одной записи!")
    
    text = ''

    for i in data:
        text+=f"{i.name}: {i.date_birth}\n"

    await message.reply(text)