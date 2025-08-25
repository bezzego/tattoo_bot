from aiogram import Bot, types
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from app import config

# Placeholders for media file IDs
PORTFOLIO_PHOTOS = [
    "AgACAgIAAxkBAAMMaKxDs1oUYyQWjy_xXKQ2ATxoIFAAAgb6MRvyMWBJlwGywBS7fuYBAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAMOaKxDtpl73leMc0iRBh0OBhYuosMAAgf6MRvyMWBJR5mXRkBsqysBAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAMQaKxDv22xW5InTUWm3q1FyNksbd8AAgj6MRvyMWBJsZMZgGBC0rIBAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAMSaKxDwtMZXxDbs0DclO_AlfIUM8gAAgn6MRvyMWBJdbbHMAlqa80BAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAMTaKxDwl-sl0Jibx2dddaLhK0cXnEAAgr6MRvyMWBJjVJNsMTbQ8sBAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAMWaKxDx6LuRxiG16cYlUCcWLCDToIAAgv6MRvyMWBJEacK8GsG2HkBAAMCAAN5AAM2BA",
]

REVIEWS_PHOTOS = [
    "AgACAgIAAxkBAAMCaKxDOGu5hwRQX-KCRzoRTOjxk3gAAv75MRvyMWBJjT3rdLkwid8BAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAMEaKxDQktYN3-DUTL9FnOaZCgn3xsAAv_5MRvyMWBJE9GBQVDcz1sBAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAMGaKxDRfgYPUIiR1FE-vBt_Oc946cAAgH6MRvyMWBJ7VnX3ed-Vl0BAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAMIaKxDSDRUkbaPNeOSqnBvflkpticAAgL6MRvyMWBJrnMkBE_7jPsBAAMCAAN5AAM2BA",
]

SKETCHES_PHOTOS = [
    "AgACAgIAAxkBAAMYaKxGt5JLV-MKVP5KQCZIZpzWdWcAAiX6MRvyMWBJX9ld6kL5qSQBAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAMZaKxGtxTauMz1xjicBD5Rvuffo1AAAib6MRvyMWBJqElZx9o5SZ4BAAMCAAN5AAM2BA",
    "AgACAgIAAxkBAAMbaKxGt8EFqaXpIrxITZfb2PxQAh0AAif6MRvyMWBJOgABZCVKIPtwAQADAgADeQADNgQ",
]


async def send_portfolio(message: types.Message, bot: Bot):
    """Send portfolio images and a button to more works."""
    if PORTFOLIO_PHOTOS:
        media = [InputMediaPhoto(media=file_id) for file_id in PORTFOLIO_PHOTOS]
        await bot.send_media_group(message.chat.id, media=media)
    if config.PORTFOLIO_URL:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Ещё работы", url=config.PORTFOLIO_URL)]
            ]
        )
        await message.answer(
            "Больше работ вы можете увидеть по ссылке:", reply_markup=kb
        )


async def send_reviews(message: types.Message, bot: Bot):
    """Send review screenshots and a button to leave a review."""
    if REVIEWS_PHOTOS:
        media = [InputMediaPhoto(media=file_id) for file_id in REVIEWS_PHOTOS]
        await bot.send_media_group(message.chat.id, media=media)
    if config.REVIEWS_URL:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Оставить отзыв", url=config.REVIEWS_URL)]
            ]
        )
        await message.answer(
            "Оставить свой отзыв можно на Яндекс.Картах по ссылке:", reply_markup=kb
        )


async def send_sketches(message: types.Message, bot: Bot):
    """Send sketch images each with an inline 'I want this' button, plus link to more sketches."""
    if SKETCHES_PHOTOS:
        for idx, file_id in enumerate(SKETCHES_PHOTOS, start=1):
            kb = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Хочу такой", callback_data=f"sketch:{idx}"
                        )
                    ]
                ]
            )
            await bot.send_photo(
                message.chat.id, file_id, caption=f"Эскиз #{idx}", reply_markup=kb
            )
    else:
        await message.answer("Список эскизов сейчас недоступен.")
    if config.SKETCHES_URL:
        link_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Больше эскизов", url=config.SKETCHES_URL)]
            ]
        )
        await message.answer(
            "Больше наших эскизов вы найдёте по ссылке:", reply_markup=link_kb
        )
