from aiogram import Router, types
from services.databases import all_services, get_user_id

router = Router()

@router.message(lambda message: message.text == "Все сервисы")
async def get_service(message: types.Message):
    username = message.from_user.username
    user_id = get_user_id(username)

    services = all_services(user_id)

    if not services:
        await message.answer("У вас пока нет сервисов")
        return

    response = "📁 Ваши сервисы:\n\n" + "\n".join(
        f"🔹 {service[0]} (логин: {service[1]})"
        for service in services
    )
    await message.answer(response)
