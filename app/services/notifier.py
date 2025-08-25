import json
import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app import config

# RU labels for dropdown/enum values
ZONES_RU = {
    "back": "спина",
    "chest": "грудь",
    "ribs": "рёбра",
    "stomach": "живот",
    "shoulder": "плечо",
    "arm": "рука",
    "forearm": "предплечье",
    "wrist": "запястье",
    "hand": "кисть",
    "neck": "шея",
    "thigh": "бедро",
    "leg": "нога",
    "ankle": "щиколотка",
    "foot": "стопа",
    "ear": "ухо",
    "face": "лицо",
}

SIZES_RU = {
    "small": "маленький",
    "medium": "средний",
    "large": "большой",
    "xl": "очень большой",
}

WORK_TYPES_RU = {
    "new": "новая татуировка",
    "coverup": "перекрытие",
    "fix": "коррекция",
    "laser": "удаление",
    "piercing": "пирсинг",
}

IDEA_TYPES_RU = {
    "image": "картинка/иллюстрация",
    "text": "текст",
    "portrait": "портрет",
    "lettering": "леттеринг",
    "minimal": "минимализм",
}


async def notify_master(bot: Bot, lead, client):
    """Send a new lead notification to the master (admin)."""
    if not config.RECEIVE_LEADS:
        # If receiving leads is turned off, do not notify
        logging.info("Lead received but notifications are off.")
        return
    # Prepare client info
    username = client.username or ""
    name_or_id = f"@{username}" if username else f"id:{client.tg_user_id}"
    phone = client.phone or "не указан"
    # Prepare message text
    if lead.source == "sketch":
        # Special format for sketch requests
        design_info = lead.comment or "(эскиз)"
        text = (
            "Новая заявка 🎯 (эскиз)\n"
            f"Клиент: {name_or_id} (id: {client.tg_user_id})\n"
            f"Телефон: {phone}\n\n"
            f"Выбранный эскиз: {design_info}\n"
        )
    else:
        ru_zone = ZONES_RU.get(getattr(lead, "zone", None), lead.zone)
        ru_size = SIZES_RU.get(getattr(lead, "size", None), lead.size)
        ru_work = WORK_TYPES_RU.get(getattr(lead, "work_type", None), lead.work_type)
        ru_idea = IDEA_TYPES_RU.get(getattr(lead, "idea", None), lead.idea)
        text = (
            "Новая заявка 🎯\n"
            f"Клиент: {name_or_id} (id: {client.tg_user_id})\n"
            f"Телефон: {phone}\n\n"
            f"Зона: {ru_zone}\n"
            f"Идея: {ru_idea}\n"
            f"Размер: {ru_size}\n"
            f"Тип работы: {ru_work}\n"
        )
        # Include references indicator if present
        if lead.references_json:
            try:
                refs = json.loads(lead.references_json)
            except json.JSONDecodeError:
                refs = []
            if refs:
                text += "Референсы: " + ", ".join(
                    f"[фото {i}]" for i, _ in enumerate(refs, start=1)
                )
                text += "\n"
        if lead.comment:
            text += f"Комментарий: {lead.comment}\n"
    # Prepare inline keyboard for quick actions
    kb_rows = [
        [
            InlineKeyboardButton(
                text="Ответить клиенту", url=f"tg://user?id={client.tg_user_id}"
            )
        ]
    ]
    if username:
        kb_rows.append(
            [
                InlineKeyboardButton(
                    text="Открыть профиль", url=f"https://t.me/{username}"
                )
            ]
        )
    kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
    # Send the message to master
    try:
        await bot.send_message(config.MASTER_ID, text, reply_markup=kb)
    except Exception as e:
        logging.error(f"Failed to send lead notification to master: {e}")
    # If there are reference photos, send them separately
    if hasattr(lead, "references_json") and lead.references_json:
        try:
            refs = json.loads(lead.references_json)
        except:
            refs = []
        for file_id in refs:
            if file_id:
                try:
                    await bot.send_photo(config.MASTER_ID, file_id)
                except Exception as e:
                    logging.error(f"Не удалось отправить фото референса: {e}")
