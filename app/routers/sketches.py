from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app import texts
from app.models import db
from app.repo import clients, leads
from app.services import notifier, media
from app.keyboards import main as main_keyboard

router = Router()


@router.message(F.text == texts.MENU_SKETCHES)
async def show_sketch_gallery(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    await message.answer("Наши эскизы:")
    await media.send_sketches(message, bot)


@router.callback_query(F.data.startswith("sketch:"))
async def handle_sketch_choice(call: CallbackQuery, bot: Bot):
    await call.answer()
    # Determine which sketch was chosen
    sketch_id = call.data.split(":", 1)[1] if call.data else ""
    design_comment = f"Эскиз #{sketch_id}" if sketch_id else "Эскиз (не указан)"
    # Save lead in database
    async with db.AsyncSessionLocal() as session:
        client = await clients.get_or_create_client(session, call.from_user)
        lead = await leads.create_lead(
            session,
            client.id,
            source="sketch",
            zone="(sketch)",
            idea="(sketch)",
            size="(sketch)",
            work_type="(sketch)",
            references=None,
            comment=design_comment,
        )
        await session.commit()
    # Notify master
    await notifier.notify_master(bot, lead, client)
    # Confirm to user
    await call.message.answer(
        "✅ Заявка на выбранный эскиз отправлена мастеру.",
        reply_markup=main_keyboard.main_menu(),
    )
