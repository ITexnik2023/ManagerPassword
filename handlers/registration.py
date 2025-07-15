from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
from aiogram.types import Message,CallbackQuery
from services.databases import register_users
router = Router()
class Registration(StatesGroup):
    email = State()
    username = State()
    password = State()
    confirm_password = State()


@router.callback_query(lambda callback: callback.data == 'register')
async def register_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.email)
    await callback.answer()  # Убираем "часики" на кнопке
    await callback.message.edit_text(
        "🔐 Регистрация\n\n📧Введите ваш email:",

        reply_markup=None  # Убираем клавиатуру после нажатия
    )

@router.message(Registration.email)
async def procces_email(message: Message, state: FSMContext):
    if not '@' in message.text:
        await message.answer("❌ Некорректный email. Попробуйте снова:")
        return
    await state.update_data(email=message.text)  # Сохраняем email
    await state.set_state(Registration.username)  # Переключаем на состояние "username"
    #проверяем наличие username
    telegram_username = message.from_user.username
    if telegram_username:
        await state.update_data(username=telegram_username)
        await state.set_state(Registration.password)
        await message.answer(
            f"🔒 Мы используем ваш Telegram username: @{telegram_username}\n"
            "Теперь придумайте пароль (минимум 8 символов):"
        )
    else:
        await state.set_state(Registration.username)
        await message.answer(
            "🔒 Мы не нашли username в вашем Telegram профиле.\n"
            "Пожалуйста, придумайте username:"
        )

@router.message(Registration.username)
async def procces_username(message: Message, state: FSMContext):
    if len(message.text) < 3:
        await message.answer("❌ Username должен быть не менее 3 символов")
        return
    await state.update_data(username=message.text)
    await state.set_state(Registration.password)  # Переключаем на состояние "password"
    await message.answer("🔒 Придумайте пароль:")

@router.message(Registration.password)
async def procces_password(message: Message, state: FSMContext):
    if len(message.text) < 8:
        await message.answer("Пароль должен быть не менее 8 символов!")
        return
    await state.update_data(password=message.text)  # Сохраняем пароль
    await state.set_state(Registration.confirm_password)  # Переключаем на состояние "confirm_password"
    await message.answer("🔒 Повторите пароль:")

@router.message(Registration.confirm_password)
async def procces_confirm_password(message: Message, state: FSMContext):
    user_data = await state.get_data()
    password_original = user_data.get('password')
    confirm_password = message.text
    if password_original != confirm_password:
        await message.answer("Пароли не совпадают:( Повторите попытку!")
        await state.set_state(Registration.password)
        await message.answer("🔒 Введите пароль еще раз")
        return

    if register_users(user_data['email'],user_data['username'] ,user_data['password']):
        await message.answer("✅ Регистрация успешно завершена!")
    else:
        await message.answer("❌ Пользователь уже существует")

    await state.clear()