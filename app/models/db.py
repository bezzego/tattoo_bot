from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.base import Base

DATABASE_URL = "sqlite+aiosqlite:///tattoo_bot.db"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    # import models to register tables
    import app.models.user
    import app.models.lead

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
