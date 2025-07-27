from dotenv import load_dotenv
import asyncio
import bot_factory
from services.databases import init_db


init_db()
async def main():
    load_dotenv()
    bot = bot_factory.create_bot()  # переменная, которая импортирует из файла config BOT_TOKEN
    dp = bot_factory.create_dispatcher()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



