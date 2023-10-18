from contextlib import AbstractAsyncContextManager
from typing import Any, Callable, Generic, Sequence, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel as BaseSchema
from sqlalchemy import delete, insert, join, select, text, update
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import ColumnExpressionArgument, Select
from sqlalchemy.sql.elements import ColumnElement

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        model: Type[ModelType],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.model = model
        self.session_factory = session_factory


class GetWhereMixin(BaseRepository[ModelType]):
    async def get_where(
        self,
        *,
        wheres: tuple[ColumnExpressionArgument[bool], ...] | None = None,
    ) -> ModelType | None:
        stmt = select(self.model)
        if wheres:
            stmt = stmt.where(*wheres)

        async with self.session_factory() as session:
            obj = await session.execute(stmt)
        return obj.scalars().first()


class GetByIDMixin(GetWhereMixin[ModelType]):
    async def get_by_id(self, id: UUID) -> ModelType | None:
        return await self.get_where(
            wheres=(getattr(self.model, "id") == id,),
        )


class GetMultiWhereMixin(BaseRepository[ModelType]):
    async def get_multi_where(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        wheres: tuple[ColumnExpressionArgument[bool], ...] | None = None,
        order_by: str | None = None,
    ) -> Sequence[ModelType] | None:
        stmt = select(self.model)
        if wheres:
            stmt = stmt.where(*wheres)

        if order_by:
            stmt = stmt.order_by(text(order_by))

        stmt = stmt.offset(offset).limit(limit)

        async with self.session_factory() as session:
            objs = await session.execute(stmt)
        return objs.scalars().all()


class GetAllMixin(GetMultiWhereMixin[ModelType]):
    async def get_all(
        self,
        offset: int = 0,
        limit: int = 100,
        order_by: str | None = None,
    ) -> Sequence[ModelType] | None:
        return await self.get_multi_where(offset=offset, limit=limit, order_by=order_by)


CreateSchemeType = TypeVar("CreateSchemeType", bound=BaseSchema)


class CreateMixin(Generic[ModelType, CreateSchemeType], BaseRepository[ModelType]):
    async def create(self, create_in: CreateSchemeType) -> ModelType:
        async with self.session_factory() as session:
            raw_obj = await session.execute(
                insert(self.model)
                .values(**create_in.model_dump())
                .returning(self.model)
            )
            await session.commit()

        return raw_obj.scalars().one()


UpdateSchemeType = TypeVar("UpdateSchemeType", bound=BaseSchema)


class UpdateWhereMixin(Generic[ModelType, UpdateSchemeType], BaseRepository[ModelType]):
    async def update_where(
        self,
        *,
        update_in: UpdateSchemeType,
        wheres: tuple[ColumnExpressionArgument[bool], ...] | None = None,
    ) -> ModelType:
        stmt = update(self.model)
        if wheres:
            stmt = stmt.where(*wheres)
        stmt = stmt.values(**update_in.model_dump(exclude_none=True)).returning(
            self.model
        )

        async with self.session_factory() as session:
            raw_obj = await session.execute(stmt)
            await session.commit()

        return raw_obj.scalars().one()


class UpdateByIDMixin(UpdateWhereMixin[ModelType, UpdateSchemeType]):
    async def update_by_id(
        self,
        update_in: UpdateSchemeType,
        id: UUID,
    ) -> ModelType:
        return await self.update_where(
            update_in=update_in,
            wheres=(getattr(self.model, "id") == id,),
        )


class DeleteWhereMixin(BaseRepository[ModelType]):
    async def delete_where(
        self,
        *,
        wheres: tuple[ColumnExpressionArgument[bool], ...] | None = None,
    ) -> None:
        stmt = delete(self.model)
        if wheres:
            stmt = stmt.where(*wheres)

        async with self.session_factory() as session:
            await session.execute(stmt)
            await session.commit()


class DeleteByIDMixin(DeleteWhereMixin[ModelType]):
    async def delete(self, id: UUID) -> None:
        await self.delete_where(wheres=(getattr(self.model, "id") == id,))


FirstModelType = TypeVar("FirstModelType", bound=Base)
SecondModelType = TypeVar("SecondModelType", bound=Base)
AssociationTable = TypeVar("AssociationTable", bound=Base)


class BaseOneToManyRepository(Generic[FirstModelType, SecondModelType]):
    def __init__(
        self,
        one_model: Type[FirstModelType],
        many_model: Type[SecondModelType],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.session_factory = session_factory

        self.one_model = one_model
        self.many_model = many_model

        to_one_fk = tuple(many_model.__table__.foreign_keys)[0]

        self.column_to_one_fk = to_one_fk.parent

        for column_one_pk in self.one_model.__table__.primary_key:
            self.column_one_pk = column_one_pk


V = TypeVar("V")


class OneToManyRepository(BaseOneToManyRepository[FirstModelType, SecondModelType]):
    async def get(
        self,
        *,
        wheres: tuple[ColumnExpressionArgument[bool], ...] | None = None,
        returns: tuple[InstrumentedAttribute[V], ...] | None = None,
    ) -> Row[tuple[V, ...]] | None:
        if returns:
            stmt = select(*returns)
        else:
            stmt = select(*(self.one_model, self.many_model))

        stmt = stmt.select_from(
            join(
                self.one_model,
                self.many_model,
                self.column_to_one_fk == self.column_one_pk,
            )
        )

        if wheres:
            stmt = stmt.where(*wheres)

        async with self.session_factory() as session:
            objs = await session.execute(stmt)

        return objs.one_or_none()


class BaseAndRepository(Generic[FirstModelType, SecondModelType, AssociationTable]):
    def __init__(
        self,
        first_model: Type[FirstModelType],
        second_model: Type[SecondModelType],
        association_model: Type[AssociationTable],
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.session_factory = session_factory

        self.first_model = first_model
        self.second_model = second_model
        self.association_model = association_model

        try:
            first_fk, second_fk = tuple(association_model.__table__.foreign_keys)
        except ValueError:
            raise ValueError(
                f"Association Model {association_model} must contain two foreign keys"
                " on first and second models."
            )

        if first_fk.column.table == first_model.__table__:
            fk_to_first_model = first_fk
            fk_to_second_model = second_fk
        else:
            fk_to_first_model = second_fk
            fk_to_second_model = first_fk

        self.column_pk_of_first_model = fk_to_first_model.column
        self.column_pk_of_second_model = fk_to_second_model.column

        association_model_columns_info_collection = (
            association_model.__table__.columns._collection
        )
        for column_info in association_model_columns_info_collection:
            column_element: ColumnElement = column_info[1]
            if fk_to_first_model in column_element.foreign_keys:
                self.column_fk_to_first_model = column_element
            elif fk_to_second_model in column_element.foreign_keys:
                self.column_fk_to_second_model = column_element


class BaseFirstAndSecondRepository(
    BaseAndRepository[FirstModelType, SecondModelType, AssociationTable]
):
    async def _get_base_stmt(
        self,
        *,
        wheres: tuple[ColumnExpressionArgument[bool], ...] | None = None,
        returns: tuple[InstrumentedAttribute[V], ...] | None = None,
        offset: int = 0,
        limit: int = 100,
        order_by: str | None = None,
    ) -> Select[Any]:
        if returns:
            stmt = select(*returns)
        else:
            stmt = select(*(self.first_model, self.second_model))

        stmt = stmt.select_from(
            join(
                self.first_model,
                self.association_model,
                self.column_pk_of_first_model == self.column_fk_to_first_model,
            ).join(
                self.second_model,
                self.column_pk_of_second_model == self.column_fk_to_second_model,
            )
        )

        if wheres:
            stmt = stmt.where(*wheres)
        if order_by:
            stmt = stmt.order_by(text(order_by))

        stmt = stmt.offset(offset).limit(limit)

        return stmt

    async def get(
        self,
        *,
        wheres: tuple[ColumnExpressionArgument[bool], ...] | None = None,
        returns: tuple[InstrumentedAttribute[V], ...] | None = None,
        offset: int = 0,
        limit: int = 100,
        order_by: str | None = None,
    ) -> Sequence[Row[tuple[V, ...]]]:
        stmt = await self._get_base_stmt(
            wheres=wheres,
            returns=returns,
            offset=offset,
            limit=limit,
            order_by=order_by,
        )
        async with self.session_factory() as session:
            objs = await session.execute(stmt)

        return objs.all()
