from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
import logging
import os

from app import texts, config

# ======= Attachments for healing sections =======
HEALING_PDFS = {
    "classic": "BQACAgIAAxkBAAIDwGiwG8lWZsdbpCJyfnfyZzemzpoiAAKehAACq6GISRcVKol2dQWENgQ",
    "film": "BQACAgIAAxkBAAIDvmiwG8V440VP1ysnnA_M9qFZHXc-AAKdhAACq6GISVbDrbjLAAGi2TYE",
    "piercing": "BQACAgIAAxkBAAIDumiwG6YELn1GJgThkyECs0fMFU-RAAKYhAACq6GISbZzAaUxdLE0NgQ",
    "removal": "BQACAgIAAxkBAAIDvGiwG7vHXmtl0NTkX8zWb-iNdsj-AAKbhAACq6GISehnj7-EDnkvNgQ",
}

HEALING_PHOTOS = {
    "classic": "AgACAgIAAxkBAAPNaKxdDvrghkXjjZRL6UCXDAuyW54AAlL7MRvyMWBJeYDWq1AuUYkBAAMCAAN5AAM2BA",
    "film": "AgACAgIAAxkBAAIDpGiwGAuhDnkAAcU-Si3GQ14K4znq3wACGvUxG6uhiElj2DoRY8ugswEAAwIAA3kAAzYE",
    "piercing": "AgACAgIAAxkBAAIDpmiwGFBiuBs80KndAyI1qdVJyHqJAAIe9TEbq6GIScQIK9zXh_00AQADAgADeQADNgQ",
    "removal": "AgACAgIAAxkBAAPKaKxdDqoCw_RK8GFw661LEaMKbWYAAk_7MRvyMWBJqdLW6-d77fMBAAMCAAN5AAM2BA",
}

HEALING_TITLES = {
    "classic": "Классическое заживление",
    "film": "Заживление под пленкой",
    "piercing": "Заживление пирсинга",
    "removal": "Уход после удаления",
}

HEALING_TEXTS = {
    "classic": texts.HEALING_CLASSIC,
    "film": texts.HEALING_FILM,
    "piercing": texts.HEALING_PIERCING,
    "removal": texts.HEALING_REMOVAL,
}
# ============================================================================

router = Router()
logger = logging.getLogger(__name__)


def get_healing_keyboard(current_topic: str = None) -> InlineKeyboardMarkup:
    """Создает клавиатуру с вариантами заживления"""
    buttons = []
    topics = ["classic", "film", "piercing", "removal"]

    # Создаем кнопки для всех тем, кроме текущей
    for topic in topics:
        if topic != current_topic:
            button_text = {
                "classic": "✨ Классическое",
                "film": "🎞 Пленка",
                "piercing": "💎 Пирсинг",
                "removal": "❌ Удаление",
            }.get(topic, topic)

            buttons.append(
                InlineKeyboardButton(text=button_text, callback_data=f"heal:{topic}")
            )

    # Добавляем кнопку связи с мастером
    buttons.append(
        InlineKeyboardButton(
            text="✉️ Написать мастеру", url=f"tg://user?id={config.MASTER_ID}"
        )
    )

    # Разбиваем на ряды по 2 кнопки
    keyboard = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.message(F.text == texts.MENU_HEALING)
async def show_healing_menu(message: Message, state: FSMContext):
    """Показывает меню выбора типа заживления"""
    await state.clear()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✨ Классическое", callback_data="heal:classic"
                ),
                InlineKeyboardButton(text="🎞 Пленка", callback_data="heal:film"),
            ],
            [
                InlineKeyboardButton(text="💎 Пирсинг", callback_data="heal:piercing"),
                InlineKeyboardButton(text="❌ Удаление", callback_data="heal:removal"),
            ],
        ]
    )

    await message.answer(
        text="🩹 <b>Выберите тип заживления:</b>",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("heal:"))
async def handle_healing_selection(call: CallbackQuery, state: FSMContext, bot):
    """Обрабатывает выбор типа заживления"""
    await call.answer()

    topic = call.data.split(":", 1)[1]

    # Получаем данные для выбранного типа
    photo_file_id = HEALING_PHOTOS.get(topic)
    title = HEALING_TITLES.get(topic, "Уход")
    text_content = HEALING_TEXTS.get(topic, "Информация временно недоступна.")

    # Создаем клавиатуру с другими вариантами
    keyboard = get_healing_keyboard(topic)

    try:
        # Отправляем фото с текстом и кнопками
        if photo_file_id:
            await call.message.answer_photo(
                photo=photo_file_id,
                caption=f"🩹 <b>{title}</b>\n\n{text_content}",
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        else:
            # Если фото нет, отправляем только текст
            await call.message.answer(
                text=f"🩹 <b>{title}</b>\n\n{text_content}",
                reply_markup=keyboard,
                parse_mode="HTML",
            )

        # Отправляем PDF файл отдельным сообщением
        pdf_file_id = HEALING_PDFS.get(topic)
        if pdf_file_id:
            try:
                await call.message.answer_document(
                    document=pdf_file_id, caption=f"📄 Памятка по {title.lower()}"
                )
            except TelegramBadRequest:
                logger.warning(f"Не удалось отправить PDF для {topic}")

    except Exception as e:
        logger.error(f"Ошибка при отправке информации о заживлении {topic}: {e}")

        # Fallback: отправляем без фото
        await call.message.answer(
            text=f"🩹 <b>{title}</b>\n\n{text_content}",
            reply_markup=keyboard,
            parse_mode="HTML",
        )

        if pdf_file_id:
            try:
                await call.message.answer_document(
                    document=pdf_file_id, caption=f"📄 Памятка по {title.lower()}"
                )
            except TelegramBadRequest:
                pass
