from aiogram import F, Router, types
from aiogram.filters.command import Command
from database import requests
from datetime import datetime
import sqlalchemy.orm.exc
router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await requests.set_user(message.from_user.id)
    await message.reply("Добро пожаловать! Воспользуйтесь командой /help чтобы получить информацию по функционалу бота")

@router.message(Command('add'))
async def add(message: types.Message):
    try:
        data = message.text.split()
        if len(data) < 3:
            return await message.reply('Пожалуйста, укажите имя и дату в формате: /add Имя Дата(dd.mm.yyyy)')
        
        name = data[1].lower()
        try:
            date = datetime.strptime(data[2], "%d.%m.%Y").date()
        except ValueError:
            return await message.reply("Некорректный формат даты. Используйте день.месяц.год, например 31.12.2000.")

        try:
            await requests.set_birthday(message.from_user.id, name, date)
        except KeyError:
            return await message.reply('Данное имя уже присуствует в таблице, укажите другое имя или добавьте цифры')

    except Exception as error:
        return await message.reply(f"Произошла непредвиденная ошибка: {str(error)}")    

    await message.reply(f'Успешно добавили дату рождения для {name.capitalize()}')

@router.message(Command('del'))
async def add(message: types.Message):
    try:
        try:
            name = message.text.split()[1].lower()
        except IndexError:
            return await message.reply("Пожалуйста, укажите имя которое желаете удалить из таблицы! В формате: /del Имя")
        
        try:
            await requests.del_birthday(message.from_user.id, name)
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            return await message.reply('Вы пытаетесь удалить несуществующие имя в таблице!')

    except Exception as error:
        return await message.reply(f"Произошла непредвиденная ошибка: {str(error)}")   

    await message.reply(f'Успешно удалили {name.capitalize()} из таблицы!')

@router.message(Command('get'))
async def add(message: types.Message):
    data = await requests.get_birthdays(message.from_user.id)
    if not data:
        return await message.reply("Вы не добавили ещё ни одной записи!")

    await message.reply("\n".join(f"{item.name.capitalize()}: {datetime.strftime(item.date_birth, '%d.%m.%Y')}" for item in data))

@router.message(Command('help'))
async def help(message: types.Message):
    await message.reply('Подсказки: \n'
                        '/add Имя Дата - Добавить дату рождение по имени\n'
                        '/del Имя - Удалить запись по имени\n'
                        '/get - Получить все записи')