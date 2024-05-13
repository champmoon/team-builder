from typing import Sequence
from uuid import UUID

from app import consts, schemas
from app.models import ExercisesTypes
from app.repositories import ExercisesTypesRepository


class ExercisesTypesService:
    def __init__(self, repository: ExercisesTypesRepository) -> None:
        self.repository = repository

    async def get_by_type(self, type: int, trainer_id: UUID) -> ExercisesTypes | None:
        return await self.repository.get_by_type(type=type, trainer_id=trainer_id)

    async def get_all(self, trainer_id: UUID) -> Sequence[ExercisesTypes]:
        return await self.repository.get_all(trainer_id=trainer_id)

    async def create(
        self, schema_in: schemas.CreateExercisesTypeIn, trainer_id: UUID
    ) -> ExercisesTypes:
        return await self.repository.create(schema_in=schema_in, trainer_id=trainer_id)

    async def update(
        self, schema_in: schemas.UpdateExercisesTypeIn, trainer_id: UUID
    ) -> ExercisesTypes:
        return await self.repository.update(schema_in=schema_in, trainer_id=trainer_id)

    async def delete(self, type: int, trainer_id: UUID) -> ExercisesTypes:
        return await self.repository.delete(type=type, trainer_id=trainer_id)

    async def delete_by_trainer_id(self, trainer_id: UUID) -> None:
        await self.repository.delete_by_trainer_id(trainer_id=trainer_id)

    async def initialize_defaults(self, trainer_id: UUID) -> None:
        for exercises_type in consts.ExercisesTypesEnum:
            exercises_type_out = await self.repository.get_by_type(
                type=exercises_type, trainer_id=trainer_id
            )
            if exercises_type_out:
                continue

            await self.repository.create(
                schema_in=schemas.CreateExercisesTypeIn(
                    type=exercises_type,
                    description=consts.EXERCISES_TYPES_DESC[exercises_type],
                    is_basic=exercises_type in list(consts.BasicExercisesTypesEnum),
                ),
                trainer_id=trainer_id,
            )
