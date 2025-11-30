from aiogram import F, Router, types
from aiogram.filters.command import Command

router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.reply("Hello world!")
    