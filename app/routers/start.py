from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app import texts
from app.keyboards import main as main_keyboard

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
    # If user is in any state (for example returning to start), clear it
    await state.clear()
    # Send welcome photo with caption and the main menu keyboard
    await message.answer_photo(
        photo="AgACAgIAAxkBAAID0GiwHS5byqQDybHBMglOuEc2P8UDAAI19TEbq6GISeheHL_fEOMfAQADAgADeQADNgQ",
        caption=texts.WELCOME_TEXT,
        reply_markup=main_keyboard.main_menu(),
    )
