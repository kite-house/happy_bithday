from aiogram import F, Router, types
from aiogram.filters.command import Command
from database import requests

router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await requests.set_user(message.from_user.id)
    await message.reply("Hello world!")
    