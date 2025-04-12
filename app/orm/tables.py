import datetime
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.orm.base import Base, TimestampBase


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    public_id: Mapped[UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        default=uuid4,
        server_default=sa.text("gen_random_uuid()"),
        nullable=False,
    )
    password: Mapped[str] = mapped_column(sa.String(128))
    last_login: Mapped[datetime.datetime | None] = mapped_column(
        sa.TIMESTAMP(timezone=True), nullable=True
    )
    is_superuser: Mapped[bool] = mapped_column(sa.Boolean, default=False)
    nickname: Mapped[str] = mapped_column(sa.String(12), unique=True)
    email: Mapped[str] = mapped_column(sa.String(255), unique=True)
    photo: Mapped[str] = mapped_column(sa.String(200), default="")
    intro: Mapped[str] = mapped_column(sa.Text, default="")
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)


class Record(TimestampBase):
    __tablename__="record"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    author: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    evaluation: Mapped[int] = mapped_column(sa.Integer, nullable=True)
    review: Mapped[str] = mapped_column(sa.String(100), nullable=True)
    commentary: Mapped[str] = mapped_column(sa.Text, nullable=True)

    __table_args__ = (
        sa.Index("ix_record_id", "id"),
        sa.Index("ix_recode_user_author_title","user_id","author","title", unique=True),
        sa.Index("ix_record_updated_at", "updated_at")
    )
