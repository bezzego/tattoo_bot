from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime, date, time
from app import config, texts
from app.keyboards import inline as inline_kb
from app.models import db, lead as lead_model
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import io, csv
from app.repo import clients

router = Router()


@router.message(Command("admin"))
async def admin_menu(message: Message):
    if message.from_user.id != config.MASTER_ID:
        await message.answer(texts.ADMIN_ONLY)
        return
    status_text = config.TOGGLE_ON if config.RECEIVE_LEADS else config.TOGGLE_OFF
    text = f"Текущий MASTER_ID: {config.MASTER_ID}\nПриём заявок: {status_text}"
    kb = inline_kb.toggle_leads_keyboard(config.RECEIVE_LEADS)
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == "toggle_leads")
async def toggle_leads(call: CallbackQuery):
    if call.from_user.id != config.MASTER_ID:
        await call.answer("Нет доступа")
        return
    config.RECEIVE_LEADS = not config.RECEIVE_LEADS
    # Update the admin menu message
    status_text = config.TOGGLE_ON if config.RECEIVE_LEADS else config.TOGGLE_OFF
    new_text = f"Текущий MASTER_ID: {config.MASTER_ID}\nПриём заявок: {status_text}"
    kb = inline_kb.toggle_leads_keyboard(config.RECEIVE_LEADS)
    try:
        await call.message.edit_text(new_text, reply_markup=kb)
    except:
        pass
    await call.answer("Настройка обновлена", show_alert=False)


@router.message(Command("set_master"))
async def set_master_cmd(message: Message):
    if message.from_user.id != config.MASTER_ID:
        await message.answer(texts.ADMIN_ONLY)
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /set_master <user_id>")
        return
    try:
        new_master_id = int(parts[1])
    except ValueError:
        await message.answer("MASTER_ID должен быть числом.")
        return
    config.MASTER_ID = new_master_id
    await message.answer(
        f"✅ MASTER_ID изменён на {new_master_id}. Новому мастеру необходимо нажать /start в боте."
    )


@router.message(Command("leads_today"))
async def leads_today_cmd(message: Message):
    if message.from_user.id != config.MASTER_ID:
        return
    today = date.today()
    start_dt = datetime.combine(today, time.min)
    end_dt = datetime.combine(today, time.max)
    async with db.AsyncSessionLocal() as session:
        result = await session.execute(
            select(lead_model.Lead)
            .options(selectinload(lead_model.Lead.client))
            .where(
                lead_model.Lead.created_at >= start_dt,
                lead_model.Lead.created_at <= end_dt,
            )
        )
        leads_list = result.scalars().all()
    if not leads_list:
        await message.answer(texts.NO_LEADS_TODAY)
    else:
        lines = [texts.LEADS_TODAY_HEADER]
        for ld in leads_list:
            client = ld.client
            client_name = client.username or (
                client.first_name if client.first_name else str(client.tg_user_id)
            )
            time_str = ld.created_at.strftime("%H:%M")
            lines.append(f"{ld.id} | {time_str} | {client_name} | {ld.zone}")
        await message.answer("\n".join(lines))


@router.message(Command("export"))
async def export_cmd(message: Message):
    if message.from_user.id != config.MASTER_ID:
        return
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer(texts.EXPORT_USAGE)
        return
    start_str, end_str = parts[1], parts[2]
    try:
        start_date = date.fromisoformat(start_str)
        end_date = date.fromisoformat(end_str)
    except Exception:
        await message.answer("Неверный формат дат. " + texts.EXPORT_USAGE)
        return
    if end_date < start_date:
        await message.answer("Ошибка: конечная дата раньше начальной.")
        return
    start_dt = datetime.combine(start_date, time.min)
    end_dt = datetime.combine(end_date, time.max)
    async with db.AsyncSessionLocal() as session:
        result = await session.execute(
            select(lead_model.Lead)
            .options(selectinload(lead_model.Lead.client))
            .where(
                lead_model.Lead.created_at >= start_dt,
                lead_model.Lead.created_at <= end_dt,
            )
        )
        leads_list = result.scalars().all()
    if not leads_list:
        await message.answer(texts.NO_LEADS_PERIOD)
        return
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "lead_id",
            "datetime",
            "client_id",
            "username",
            "phone",
            "source",
            "zone",
            "idea",
            "size",
            "work_type",
            "status",
        ]
    )
    for ld in leads_list:
        client = ld.client
        writer.writerow(
            [
                ld.id,
                ld.created_at.strftime("%Y-%m-%d %H:%M"),
                client.tg_user_id,
                client.username or "",
                client.phone or "",
                ld.source,
                ld.zone or "",
                ld.idea or "",
                ld.size or "",
                ld.work_type or "",
                ld.status,
            ]
        )
    output.seek(0)
    file_data = io.BytesIO(output.getvalue().encode("utf-8"))
    file_data.name = f"leads_{start_date}_{end_date}.csv"
    await message.answer_document(
        file_data, caption=f"Заявки с {start_date} по {end_date}"
    )


@router.message(Command("delete_me"))
async def delete_me_cmd(message: Message):
    # Allows any user to delete their data
    async with db.AsyncSessionLocal() as session:
        await clients.delete_client(session, message.from_user.id)
        await session.commit()
    await message.answer(texts.DELETE_DONE)
