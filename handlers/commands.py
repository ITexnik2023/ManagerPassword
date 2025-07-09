from aiogram import Router
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart
import handlers.keyboards as kb
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в менеджер паролей!', reply_markup=kb.menu)

