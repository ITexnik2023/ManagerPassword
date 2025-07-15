import sqlite3
from handlers.keyboards import main_menu
import bcrypt
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router
from aiogram.types import Message, CallbackQuery

router = Router()

class Login(StatesGroup):
    email = State()
    password = State()

@router.callback_query(lambda callback: callback.data == 'login')
async def login_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Login.email)
    await callback.answer()
    await callback.message.edit_text("Вход\n\nВведите email:", reply_markup=None)

@router.message(Login.email)
async def password_callback(message: Message, state: FSMContext):
    if not '@' in message.text:
        await message.answer("❌ Некорректный email. Попробуйте снова:")
        return
    await state.update_data(email=message.text)
    await state.set_state(Login.password)
    await message.answer("Введите пароль:")

@router.message(Login.password)
async def procces_password(message: Message, state: FSMContext):
    user_data = await state.get_data()  # Потом получаем
    email = user_data.get('email')
    password = message.text  # Пароль из состояния

    if not email or not password:
        await message.answer("❌ Ошибка в данных. Начните заново.")
        await state.set_state(Login.email)
        await state.clear()
        return



    try:
        with sqlite3.connect('db_manager_password.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if not cursor.fetchone():
                await message.answer("❌ Системная ошибка. Попробуйте позже.")
                await state.clear()
                return

            cursor.execute("""
            SELECT password_hash
            FROM users
            WHERE email = ?
            """, (email,))

            result = cursor.fetchone()
            if not result:
                await message.answer("Пользователь с таким email не найден")
                await state.set_state(Login.email)
                return
            stored_hash = result[0].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                await message.answer("✅ Вход выполнен!\nДобро пожаловать, что хотите сделать!",
                                     reply_markup=main_menu()  # Вот здесь добавляем клавиатуру
                )
            else:
                await message.answer("❌ Неверные данные")
                await state.set_state(Login.email)

    except sqlite3.Error as e:
        await message.answer(f"⚠ Ошибка базы данных: {e}")

    except Exception as e:
        await message.answer(f"⚠ Ошибка: {e}")
        return False
    finally:
        await state.clear()