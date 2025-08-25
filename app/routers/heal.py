from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app import texts, config

router = Router()


@router.message(F.text == texts.MENU_HEALING)
async def show_healing_menu(message: Message, state: FSMContext):
    await state.clear()
    # Offer sub-options via inline keyboard
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("Классическое", callback_data="heal:classic"))
    kb.add(InlineKeyboardButton("Пленка", callback_data="heal:film"))
    kb.add(InlineKeyboardButton("Пирсинг", callback_data="heal:piercing"))
    kb.add(InlineKeyboardButton("Удаление", callback_data="heal:removal"))
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
    if text_to_send:
        # Include prompt to contact master
        text_to_send = text_to_send + "\n\n" + texts.ASK_MASTER
        # Inline button to write to master
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

        kb = InlineKeyboardMarkup()
        kb.add(
            InlineKeyboardButton(
                "✉️ Написать мастеру", url=f"tg://user?id={config.MASTER_ID}"
            )
        )
        await call.message.answer(text_to_send, reply_markup=kb)
