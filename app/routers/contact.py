from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app import texts, config

router = Router()


@router.message(F.text == texts.MENU_CONTACT)
async def contact_master(message: Message, state: FSMContext):
    await state.clear()
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✉️ Написать мастеру", url=f"tg://user?id={config.MASTER_ID}"
                )
            ]
        ]
    )
    await message.answer(texts.CONTACT_INSTRUCTION, reply_markup=kb)
