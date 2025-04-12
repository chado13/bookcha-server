from __future__ import annotations

from asyncio import current_task
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.config import CONFIG


class DB:
    def __init__(self, db_url: str, *, is_pgbouncer: bool = False) -> None:
        if is_pgbouncer:
            self._engine = create_async_engine(
                db_url,
                poolclass=NullPool,
            )
        else:
            self._engine = create_async_engine(
                db_url,
                echo=False,
                pool_size=CONFIG.db_pool_size,
                max_overflow=CONFIG.db_pool_max_overflow,
                pool_pre_ping=True,
                pool_use_lifo=True,
            )
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autoflush=False,
                expire_on_commit=False,
                class_=AsyncSession,
                bind=self._engine,
            ),
            scopefunc=current_task,
        )

    async def make_session(self) -> AsyncSession:
        # async_scoped_session을 사용하기 위해서는 async로 함수를 정의하여 사용해야 합니다.
        return self._session_factory()

    async def remove_session_factory(self) -> None:
        await self._session_factory.remove()

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
            if session.is_active:
                await session.commit()
        finally:
            await self._session_factory.remove()


db = DB(CONFIG.db_url)
