from __future__ import annotations

import datetime
import uuid
from typing import Any

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import CHAR, TypeDecorator

UUIDTYPEDecorator = TypeDecorator[uuid.UUID]


class GUID(UUIDTYPEDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect: sa.engine.interfaces.Dialect) -> Any:
        if dialect.name == "postgresql":
            return dialect.type_descriptor(pg.UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(
        self, value: Any | None, dialect: sa.engine.interfaces.Dialect
    ) -> Any:
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(
        self, value: Any | None, dialect: sa.engine.interfaces.Dialect
    ) -> None | uuid.UUID:
        if value is None:
            return value
        else:
            return uuid.UUID(str(value))


class Base(DeclarativeBase):
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    type_annotation_map = {
        uuid.UUID: GUID,
    }

    def update(self, values: dict[str, Any]) -> None:
        for field, value in values.items():
            setattr(self, field, value)


class TimestampBase(Base):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), default=sa.func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        default=sa.func.now(),
        onupdate=sa.func.now(),
    )


class OrderModelIntegerId(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, nullable=False)


class OrderModelUUIDId(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, nullable=False)
