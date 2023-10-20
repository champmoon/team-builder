from contextlib import AbstractAsyncContextManager
from typing import Callable, Type

from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SportsmansGroups
from app.schemas import CreateSportsmanGroupIn, DeleteSportsmanGroupIn


class SportsmansGroupsRepository:
    def __init__(
        self,
        model: Type[SportsmansGroups],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    async def create(self, schema_in: CreateSportsmanGroupIn) -> SportsmansGroups:
        async with self.session_factory() as session:
            created_sportsman = await session.execute(
                insert(self.model)
                .values(**schema_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return created_sportsman.scalars().one()

    async def delete(self, schema_in: DeleteSportsmanGroupIn) -> SportsmansGroups:
        stmt = (
            delete(self.model)
            .where(
                self.model.group_id == schema_in.group_id,
                self.model.sportsman_id == schema_in.sportsman_id,
            )
            .returning(self.model)
        )

        async with self.session_factory() as session:
            deleted_sportsman = await session.execute(stmt)
            await session.commit()

        return deleted_sportsman.scalars().one()
