from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app import texts
from app.services import media

router = Router()


@router.message(F.text == texts.MENU_REVIEWS)
async def show_reviews(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    await message.answer(texts.REVIEWS_INTRO)
    await media.send_reviews(message, bot)
