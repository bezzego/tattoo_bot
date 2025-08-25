from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app import texts

router = Router()


@router.message(F.text == texts.MENU_ABOUT)
async def about_us(message: Message, state: FSMContext):
    await state.clear()
    # Send photo (replace with actual file_id or FSInputFile path)
    await message.answer_photo(
        photo="AgACAgIAAxkBAAIBEWisX97G1rl8kmY9yK587AbciTI0AAJf-zEb8jFgSbVc90tY54CNAQADAgADeQADNgQ",
        caption=texts.ABOUT_TEXT,
    )
