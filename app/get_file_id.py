import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()  # подтягиваем BOT_TOKEN из .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Укажи BOT_TOKEN в .env")

# Новый способ для aiogram 3.7+
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


@dp.message(F.photo)
async def handle_photo(message: Message):
    file_id = message.photo[-1].file_id
    await message.answer(f"file_id: <code>{file_id}</code>")


# Handler for document (PDF or any file)
@dp.message(F.document)
async def handle_document(message: Message):
    file_id = message.document.file_id
    await message.answer(f"file_id: <code>{file_id}</code>")


async def main():
    print("Запусти бота, пришли ему фото, и он ответит file_id")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
