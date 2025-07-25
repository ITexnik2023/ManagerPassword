from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types
from aiogram.types import Message, ReplyKeyboardRemove
from services.databases import services_users, get_user_id
from handlers.keyboards import back_kb, main_menu
router = Router()

class AddService(StatesGroup):
    name_service = State()
    login_service = State()
    password_service = State()

@router.message(lambda message: message.text == "Назад")
async def handle_back(message: types.Message, state: FSMContext):
    current_state = await state.get_data()
    if current_state is None:
        await message.answer("Выберите действие", reply_markup=main_menu())
        return
    await state.clear()
    await message.answer("Выберите действие", reply_markup=main_menu())

@router.message(lambda message: message.text == "Добавить сервис")
async def add_service_start(message: types.Message, state: FSMContext):
    await state.set_state(AddService.name_service)
    await message.answer("Введите название сервиса:", reply_markup=back_kb())



@router.message(AddService.name_service)
async def procces_name(message: Message, state: FSMContext):
    if message.text == "Назад":
        await handle_back(message, state)
        return
    await state.update_data(name_service=message.text)
    await state.set_state(AddService.login_service)
    await message.answer("Добавьте логин от сервиса:", reply_markup=back_kb())

@router.message(AddService.login_service)
async def process_login(message: Message, state: FSMContext):
    if message.text == "Назад":
        await handle_back(message, state)
        return
    await state.update_data(login_service=message.text)
    await state.set_state(AddService.password_service)
    await message.answer("Напишите пароль от сервиса:", reply_markup=back_kb())

@router.message(AddService.password_service)
async def process_password(message: Message, state: FSMContext):
    if message.text == "Назад":
        await handle_back(message, state)
        return
    try:
        data = await state.get_data()
        username = message.from_user.username
        if not username:
            await message.answer("❌ У вас не установлен username в Telegram")
            await state.clear()
            return

        user_id = get_user_id(username)
        if not user_id:
            await message.answer("❌ Пользователь не найден. Сначала зарегистрируйтесь!")
            await state.clear()
            return

        succes = services_users(user_id=user_id,
                            name_service=data["name_service"],
                            login_service=data["login_service"],
                            password_service=message.text)
        if succes:
            await message.answer(
                f"✅ Сервис добавлен!\n"
                f"Название: {data['name_service']}\n"
                f"Логин: {data['login_service']}\n"
                f"Пароль: {'*' * 8}", reply_markup=back_kb()
            )
        else:
            await message.answer("❌ Ошибка при сохранении сервиса")
    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer("❌ Произошла ошибка при обработке запроса")
    finally:
        await state.clear()

