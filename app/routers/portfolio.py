from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app import texts
from app.services import media

router = Router()


@router.message(F.text == texts.MENU_PORTFOLIO)
async def show_portfolio(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    # Introduce portfolio and send images
    await message.answer(texts.PORTFOLIO_INTRO)
    await media.send_portfolio(message, bot)
