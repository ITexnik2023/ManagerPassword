from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def login_register_kb():
    menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Зарегистрироваться', callback_data='register')],
        [InlineKeyboardButton(text='Войти', callback_data='login')]
    ])
    return  menu

def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить сервис"), KeyboardButton(text="Все сервисы")],
            [KeyboardButton(text="Удалить сервис"), KeyboardButton(text="Найти сервис")]
        ], resize_keyboard=True
    )
    return keyboard

def back_kb():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад")]
        ], resize_keyboard=True
    )
    return keyboard