from aiogram import Router
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart
from handlers.keyboards import login_register_kb

from handlers.login import procces_password
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в менеджер паролей!', reply_markup=login_register_kb())

#@router.message()

