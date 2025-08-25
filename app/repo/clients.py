from sqlalchemy import select, delete
from app.models.user import Client
from app.models.lead import Lead


async def get_or_create_client(session, tg_user):
    """Get client by Telegram user or create if not exists. Update username/fields if changed."""
    result = await session.execute(
        select(Client).where(Client.tg_user_id == tg_user.id)
    )
    client = result.scalar_one_or_none()
    if client:
        updated = False
        # update username or names if changed
        if tg_user.username and client.username != tg_user.username:
            client.username = tg_user.username
            updated = True
        if tg_user.first_name and client.first_name != tg_user.first_name:
            client.first_name = tg_user.first_name
            updated = True
        if tg_user.last_name and client.last_name != tg_user.last_name:
            client.last_name = tg_user.last_name
            updated = True
        if updated:
            await session.flush()
    else:
        client = Client(
            tg_user_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
        )
        session.add(client)
        await session.flush()  # flush to assign client.id
    return client


async def update_client_phone(session, client: Client, phone: str):
    """Update client's phone number."""
    client.phone = phone
    await session.flush()
    return client


async def delete_client(session, tg_user_id: int):
    """Delete a client and their leads from the database."""
    result = await session.execute(
        select(Client).where(Client.tg_user_id == tg_user_id)
    )
    client = result.scalar_one_or_none()
    if client:
        # delete leads first due to foreign key
        await session.execute(delete(Lead).where(Lead.client_id == client.id))
        await session.delete(client)
