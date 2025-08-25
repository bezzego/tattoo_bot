from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base, TimestampMixin


class Client(Base, TimestampMixin):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_user_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
