from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from app import texts
from app.states.quote import QuoteForm
from app.keyboards import inline as inline_kb
from app.keyboards import main as main_keyboard
from app.models import db
from app.repo import clients, leads
from app.services import notifier

router = Router()


@router.message(F.text == texts.MENU_CALCULATE)
async def start_quote_flow(message: Message, state: FSMContext):
    # Start the quote quiz flow
    await state.clear()
    # Send intro text with "Начнем" button
    await message.answer(
        texts.QUOTE_INTRO, reply_markup=inline_kb.start_quote_keyboard()
    )


@router.callback_query(F.data == "start_quote")
async def start_quote_callback(call: CallbackQuery, state: FSMContext):
    await call.answer()
    # Set initial state and ask first question (Zone)
    await state.set_state(QuoteForm.zone)
    await call.message.answer(
        texts.QUESTION_ZONE, reply_markup=inline_kb.zone_keyboard()
    )


@router.callback_query(F.data.startswith("zone:"))
async def choose_zone(call: CallbackQuery, state: FSMContext):
    await call.answer()
    zone_value = call.data.split(":", 1)[1] if call.data else ""
    # Save zone selection
    await state.update_data(zone=zone_value)
    # Move to next state
    await state.set_state(QuoteForm.idea)
    await call.message.answer(
        texts.QUESTION_IDEA, reply_markup=inline_kb.idea_keyboard()
    )


@router.callback_query(F.data.startswith("idea:"))
async def choose_idea(call: CallbackQuery, state: FSMContext):
    await call.answer()
    idea_value = call.data.split(":", 1)[1] if call.data else ""
    await state.update_data(idea=idea_value)
    await state.set_state(QuoteForm.size)
    await call.message.answer(
        texts.QUESTION_SIZE, reply_markup=inline_kb.size_keyboard()
    )


@router.callback_query(F.data.startswith("size:"))
async def choose_size(call: CallbackQuery, state: FSMContext):
    await call.answer()
    size_value = call.data.split(":", 1)[1] if call.data else ""
    await state.update_data(size=size_value)
    await state.set_state(QuoteForm.work_type)
    await call.message.answer(
        texts.QUESTION_WORK_TYPE, reply_markup=inline_kb.work_type_keyboard()
    )


@router.callback_query(F.data.startswith("work:"))
async def choose_work_type(call: CallbackQuery, state: FSMContext):
    await call.answer()
    work_value = call.data.split(":", 1)[1] if call.data else ""
    await state.update_data(work_type=work_value)
    # Next step: ask for references
    await state.set_state(QuoteForm.references)
    # Prompt user to send photos or press "Done"
    await call.message.answer(
        texts.PROMPT_REFERENCES, reply_markup=inline_kb.done_refs_keyboard()
    )


@router.message(QuoteForm.references, F.content_type == ContentType.PHOTO)
async def handle_reference_photo(message: Message, state: FSMContext):
    # User sent a photo reference
    data = await state.get_data()
    # Get current list of references from data or init new list
    refs = data.get("references", [])
    if len(refs) < 3:
        # Save file_id of the largest size photo
        if message.photo:
            file_id = message.photo[-1].file_id
            refs.append(file_id)
            await state.update_data(references=refs)
        # Acknowledge receipt
        if len(refs) < 3:
            await message.answer(
                "Фото получено. Вы можете отправить ещё или нажмите 'Готово', если завершили."
            )
        else:
            # Reached 3 photos
            await message.answer("Получено 3 фото. Нажмите 'Готово', чтобы продолжить.")
    else:
        await message.answer(
            "Вы уже отправили максимум 3 фото. Нажмите 'Готово' для продолжения."
        )


@router.callback_query(F.data == "refs_done")
async def done_references(call: CallbackQuery, state: FSMContext):
    await call.answer()
    # Move to contact state
    await state.set_state(QuoteForm.contact)
    # Ask for contact, provide phone button and skip option
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    contact_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BTN_SEND_PHONE, request_contact=True)],
            [KeyboardButton(text=texts.BTN_SKIP_PHONE)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await call.message.answer(texts.PROMPT_CONTACT, reply_markup=contact_kb)


@router.message(QuoteForm.contact, F.content_type == ContentType.CONTACT)
async def handle_contact(message: Message, state: FSMContext):
    # User shared their phone number
    phone = message.contact.phone_number if message.contact else None
    if phone:
        # Save phone in FSM data
        await state.update_data(phone=phone)
    # Now proceed to confirmation
    await go_to_confirmation(message, state)


@router.message(QuoteForm.contact, F.text == texts.BTN_SKIP_PHONE)
async def skip_contact(message: Message, state: FSMContext):
    # User chose to skip providing phone
    await state.update_data(phone=None)
    await go_to_confirmation(message, state)


async def go_to_confirmation(message: Message, state: FSMContext):
    # Gather all collected data and present confirmation
    data = await state.get_data()
    zone = data.get("zone", "")
    idea = data.get("idea", "")
    size = data.get("size", "")
    work_type = data.get("work_type", "")
    phone = data.get("phone")
    phone_text = phone if phone else "не указан"
    refs = data.get("references", [])
    refs_text = f"{len(refs)} фото" if refs else "не приложены"
    # Create confirmation text
    confirm_text = texts.CONFIRM_TEMPLATE.format(
        zone=zone,
        idea=idea,
        size=size,
        work_type=work_type,
        phone=phone_text,
        refs=refs_text,
    )
    # Switch to confirm state
    await state.set_state(QuoteForm.confirm)
    # Show summary with inline "Send" button
    await message.answer(confirm_text, reply_markup=inline_kb.confirm_keyboard())


@router.callback_query(F.data == "send_app")
async def confirm_send_application(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer()
    data = await state.get_data()
    # Create or update client in DB and save lead
    async with db.AsyncSessionLocal() as session:
        client = await clients.get_or_create_client(session, call.from_user)
        # Update phone if provided
        if data.get("phone"):
            await clients.update_client_phone(session, client, data["phone"])
        # Create lead entry
        lead = await leads.create_lead(
            session,
            client.id,
            source="quote",
            zone=data.get("zone", ""),
            idea=data.get("idea", ""),
            size=data.get("size", ""),
            work_type=data.get("work_type", ""),
            references=data.get("references", []),
            comment=None,
        )
        await session.commit()
    # Notify master
    await notifier.notify_master(bot, lead, client)
    # Clear state and thank user
    await state.clear()
    await call.message.answer(texts.APP_SENT, reply_markup=main_keyboard.main_menu())
