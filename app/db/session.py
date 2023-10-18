from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.conf.settings import settings

async_engine = create_async_engine(
    str(settings.ASYNC_SQLALCHEMY_DATABASE_URI), pool_pre_ping=True
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class DB:
    def __init__(self) -> None:
        self._engine = async_engine
        self._session_factory = async_scoped_session(
            async_sessionmaker(
                bind=async_engine,
                expire_on_commit=False,
                class_=AsyncSession,
            ),
            self.session,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        finally:
            await session.close()
