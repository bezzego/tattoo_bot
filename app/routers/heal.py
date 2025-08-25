from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext

from app import texts, config
import os

# ======= Attachments for healing sections (replace with real file_ids) =======
HEALING_PDFS = {
    "classic": "app/assets/healing/classic.pdf",
    "film": "app/assets/healing/film.pdf",
    "piercing": "app/assets/healing/piercing.pdf",
    "removal": "app/assets/healing/removal.pdf",
}
HEALING_PHOTOS = {
    "classic": [
        "AgACAgIAAxkBAAPNaKxdDvrghkXjjZRL6UCXDAuyW54AAlL7MRvyMWBJeYDWq1AuUYkBAAMCAAN5AAM2BA",
    ],
    "film": [
        "AgACAgIAAxkBAAPMaKxdDhCSswbHiyrAh4ShStGkcQkAAlH7MRvyMWBJrkJi0uOeE0wBAAMCAAN5AAM2BA",
    ],
    "piercing": [
        "AgACAgIAAxkBAAPLaKxdDpManRnQoBrdvWE6tQdUqNEAAlD7MRvyMWBJhJeD_QzwIWkBAAMCAAN5AAM2BA",
    ],
    "removal": [
        "AgACAgIAAxkBAAPKaKxdDqoCw_RK8GFw661LEaMKbWYAAk_7MRvyMWBJqdLW6-d77fMBAAMCAAN5AAM2BA",
    ],
}
# ============================================================================

router = Router()


@router.message(F.text == texts.MENU_HEALING)
async def show_healing_menu(message: Message, state: FSMContext):
    await state.clear()
    # Offer sub-options via inline keyboard
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Классическое", callback_data="heal:classic"),
                InlineKeyboardButton(text="Пленка", callback_data="heal:film"),
            ],
            [
                InlineKeyboardButton(text="Пирсинг", callback_data="heal:piercing"),
                InlineKeyboardButton(text="Удаление", callback_data="heal:removal"),
            ],
        ]
    )
    await message.answer(texts.HEALING_PROMPT, reply_markup=kb)


@router.callback_query(F.data.startswith("heal:"))
async def send_healing_info(call: CallbackQuery):
    await call.answer()
    topic = call.data.split(":", 1)[1] if call.data else ""
    text_to_send = ""
    if topic == "classic":
        text_to_send = texts.HEALING_CLASSIC
    elif topic == "film":
        text_to_send = texts.HEALING_FILM
    elif topic == "piercing":
        text_to_send = texts.HEALING_PIERCING
    elif topic == "removal":
        text_to_send = texts.HEALING_REMOVAL

    # Try to attach PDF and photos for the selected topic (if file_ids are configured)
    pdf_val = HEALING_PDFS.get(topic)
    if pdf_val and isinstance(pdf_val, str) and pdf_val:
        try:
            if os.path.exists(pdf_val):
                await call.message.answer_document(
                    document=FSInputFile(pdf_val),
                    caption=f"Памятка по заживлению ({topic})",
                )
            else:
                # Fallback: treat as Telegram file_id
                await call.message.answer_document(
                    document=pdf_val,
                    caption=f"Памятка по заживлению ({topic})",
                )
        except Exception:
            pass

    photos = HEALING_PHOTOS.get(topic, [])
    for ph in photos or []:
        if isinstance(ph, str) and ph and not ph.startswith("FILE_ID_"):
            try:
                await call.message.answer_photo(photo=ph)
            except Exception:
                pass

    if text_to_send:
        # Include prompt to contact master
        text_to_send = text_to_send + "\n\n" + texts.ASK_MASTER
        # Inline button to write to master
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✉️ Написать мастеру",
                        url=f"tg://user?id={config.MASTER_ID}",
                    )
                ],
            ]
        )
        await call.message.answer(text_to_send, reply_markup=kb)
