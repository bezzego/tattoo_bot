from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.models.base import Base, TimestampMixin


class Lead(Base, TimestampMixin):
    __tablename__ = "leads"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    source: Mapped[str] = mapped_column()
    zone: Mapped[str] = mapped_column(nullable=True)
    idea: Mapped[str] = mapped_column(nullable=True)
    size: Mapped[str] = mapped_column(nullable=True)
    work_type: Mapped[str] = mapped_column(nullable=True)
    references_json: Mapped[str] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(default="new")
    # Relationship back to client
    client: Mapped["Client"] = relationship("Client")
