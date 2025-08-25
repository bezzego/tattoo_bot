import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from app import config, logging_conf  # Initialize logging and config
from app.routers import main_router
from app.models import db


async def main():
    # Initialize bot and dispatcher
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())
    # Initialize database (create tables if not exist)
    await db.init_db()
    # Include all routers
    dp.include_router(main_router)
    # Start polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
