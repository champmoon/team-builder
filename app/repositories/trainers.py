from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Trainers
from app.schemas.trainers import CreateTrainerInDB, UpdateTrainerIn


class TrainersRepository:
    def __init__(
        self,
        model: Type[Trainers],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_id(self, id: UUID) -> Trainers | None:
        stmt = select(self.model).where(self.model.id == id)

        async with self.session_factory() as session:
            getted_trainer = await session.execute(stmt)

        return getted_trainer.scalars().first()

    async def get_by_email(self, email: str) -> Trainers | None:
        stmt = select(self.model).where(self.model.email == email)

        async with self.session_factory() as session:
            getted_trainer = await session.execute(stmt)

        return getted_trainer.scalars().first()

    async def get_all(self) -> Sequence[Trainers]:
        stmt = select(self.model)

        async with self.session_factory() as session:
            getted_trainers = await session.execute(stmt)

        return getted_trainers.scalars().all()

    async def create(self, schema_in: CreateTrainerInDB) -> Trainers:
        async with self.session_factory() as session:
            created_trainer = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_trainer.scalars().one()

    async def update(self, id: UUID, schema_in: UpdateTrainerIn) -> Trainers:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**schema_in.model_dump(exclude_none=True))
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_trainer = await session.execute(stmt)
            await session.commit()

        return updated_trainer.scalars().one()

    async def update_avatar(self, id: UUID, avatar_uri: str) -> Trainers:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(avatar_uri=avatar_uri)
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_trainer = await session.execute(stmt)
            await session.commit()

        return updated_trainer.scalars().one()

    async def delete(self, id: UUID) -> Trainers:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)

        async with self.session_factory() as session:
            deleted_trainer = await session.execute(stmt)
            await session.commit()

        return deleted_trainer.scalars().one()
