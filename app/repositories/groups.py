from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence, Type
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Groups
from app.schemas.groups import CreateGroupInDB, UpdateGroupIn


class GroupsRepository:
    def __init__(
        self,
        model: Type[Groups],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def get_by_id(self, id: UUID) -> Groups | None:
        stmt = select(self.model).where(self.model.id == id)

        async with self.session_factory() as session:
            getted_group = await session.execute(stmt)

        return getted_group.scalars().first()

    async def get_all_by_trainer_id(self, trainer_id: UUID) -> Sequence[Groups]:
        stmt = select(self.model).where(self.model.trainer_id == trainer_id)

        async with self.session_factory() as session:
            getted_group = await session.execute(stmt)

        return getted_group.scalars().all()

    async def get_all(self) -> Sequence[Groups]:
        stmt = select(self.model)

        async with self.session_factory() as session:
            getted_Groups = await session.execute(stmt)

        return getted_Groups.scalars().all()

    async def create(self, schema_in: CreateGroupInDB) -> Groups:
        async with self.session_factory() as session:
            created_group = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_group.scalars().one()

    async def update(self, id: UUID, schema_in: UpdateGroupIn) -> Groups:
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**schema_in.model_dump(exclude_none=True))
            .returning(self.model)
        )

        async with self.session_factory() as session:
            updated_group = await session.execute(stmt)
            await session.commit()

        return updated_group.scalars().one()

    async def delete(self, id: UUID) -> Groups:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)

        async with self.session_factory() as session:
            deleted_group = await session.execute(stmt)
            await session.commit()

        return deleted_group.scalars().one()
