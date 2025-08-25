from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app import texts

router = Router()


@router.message(F.text == texts.MENU_ABOUT)
async def about_us(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.ABOUT_TEXT)
