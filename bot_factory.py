from aiogram import Bot, Dispatcher #основные модули для работы с ботом
from config import settings #Класс настроек в котором находятся BOT_TOKEN и путь к базе данных
from pathlib import Path #для динамической загрузки модулей
import logging #для логирования процессов
import importlib #для динамической загрузки модулей
from typing import List, TypeVar #аннотация типа для роутеров

logger = logging.getLogger(__name__)
RouterType = TypeVar('RouterType')
def create_bot() -> Bot:
    try:
        if not settings.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не задан в настройках")
        logging.info("Создание экземпляра бота")
        return Bot(token=settings.BOT_TOKEN)

    except Exception as e:
        logger.error(f"Ошибка:{e}")
        raise

def dinamic_load_router() -> List[RouterType]:
    routers = []
    handlers_dir = Path("handlers")

    for file in handlers_dir.glob("*.py"):
        if file.stem == "__init__":
            continue
        try:
            module = importlib.import_module(f"handlers.{file.stem}")
            if hasattr(module, "router"):
                routers.append(module.router)
                logger.debug(f"Загружен роутер из папки handlers{file.stem}")
        except Exception as e:
            logger.warning(f"Не удалось загрузить {file.stem}:{e}")

    return routers

def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    for router in dinamic_load_router():
        dp.include_router(router)
        logger.debug(f"Подключен роутер:{router}")
    logger.info(f"Всего подключено роутеров: {len(dp.sub_routers)}")
    return dp