from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from config import BOT_TOKEN
import asyncio
import os
from handlers.commands import router as command_router
from handlers.registration import router as registr_router
from handlers.login import router as login_router
from handlers.add_service import router as add_service_router
from handlers.all_service import router as all_service_router
from handlers.search_service import router as search_router

from services.databases import init_db


init_db()
async def main():
    load_dotenv()
    bot = Bot(token=os.environ.get('BOT_TOKEN'))  # переменная, которая импортирует из файла config BOT_TOKEN
    dp = Dispatcher()  # Принимает входящие сообщения → Передаёт их вашим функциям → Отправляет ответы через bot.
    dp.include_router(command_router)
    dp.include_router(registr_router)
    dp.include_router(login_router)
    dp.include_router(add_service_router)
    dp.include_router(all_service_router)
    dp.include_router(search_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



