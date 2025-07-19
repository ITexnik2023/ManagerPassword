from aiogram import Router, types
from services.databases import all_services, get_user_id
from handlers.keyboards import back_kb, main_menu
router = Router()

@router.message(lambda message: message.text == "Назад")
async def back_menu(message: types.Message):
    await message.answer("Выберите действие", reply_markup=main_menu())

@router.message(lambda message: message.text == "Все сервисы")
async def get_service(message: types.Message):
    if message.text == "Назад":
        await back_menu()
        return
    username = message.from_user.username
    user_id = get_user_id(username)

    services = all_services(user_id)

    if not services:
        await message.answer("У вас пока нет сервисов", reply_markup=back_kb())
        return

    response = "📁 Ваши сервисы:\n\n" + "\n".join(
        f"🔹 {service[0]} (логин: {service[1]})"
        for service in services
    )
    await message.answer(response, reply_markup=back_kb())
