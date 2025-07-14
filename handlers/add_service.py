from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types
from aiogram.types import Message, ReplyKeyboardRemove
router = Router()

class AddService(StatesGroup):
    name_service = State()
    login_service = State()
    password_service = State()

@router.message(lambda message: message.text == "Добавить сервис")
async def add_service_start(message: types.Message, state: FSMContext):
    await state.set_state(AddService.name_service)
    await message.answer("Введите название сервиса:", reply_markup=ReplyKeyboardRemove())

@router.message(AddService.name_service)
async def procces_name(message: Message, state: FSMContext):
    await state.update_data(name_service=message.text)
    await state.set_state(AddService.login_service)
    await message.answer("Добавьте логин от сервиса:")

@router.message(AddService.login_service)
async def process_login(message: Message, state: FSMContext):
    await state.update_data(login_service=message.text)
    await state.set_state(AddService.password_service)
    await message.answer("Напишите пароль от сервиса:")

@router.message(AddService.password_service)
async def process_password(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        f"✅ Сервис добавлен!\n"
        f"Название: {data['name_service']}\n"
        f"Логин: {data['login_service']}\n"
        f"Пароль: {message.text}"
    )
    await state.clear()
