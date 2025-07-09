import sqlite3

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
    await state.update_data(password=message.text)  # Сначала сохраняем
    user_data = await state.get_data()  # Потом получаем
    email = user_data.get('email')
    password = user_data.get('password')  # Пароль из состояния

    if not email or not password:
        await message.answer("❌ Ошибка в данных. Начните заново.")
        await state.clear()
        return
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT password_hash
        FROM users
        WHERE username = ?
        """, (email))

        result = cursor.fetchone()
        if not result:
            await message.answer("Пользователь с таким email не найден")
            return False
        if bcrypt.checkpw(password.encode(), result[0]):
            await message.answer("✅ Вход выполнен!")
            await state.clear()
            return True
        else:
            await message.answer("❌ Неверные данные")
            return False
    except sqlite3.Error as e:
        await message.answer(f"⚠ Ошибка базы данных: {e}")
        return False
    except Exception as e:
        await message.answer(f"⚠ Ошибка: {e}")
        return False
    finally:
        conn.close()