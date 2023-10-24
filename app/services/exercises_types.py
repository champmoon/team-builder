from typing import Sequence

from app.consts import ExercisesTypesEnum
from app.models import ExercisesTypes
from app.repositories import ExercisesTypesRepository


class ExercisesTypesService:
    def __init__(self, repository: ExercisesTypesRepository) -> None:
        self.repository = repository

    async def get_by_type(self, type: ExercisesTypesEnum) -> ExercisesTypes | None:
        return await self.repository.get_by_type(type=type)

    async def get_all(self) -> Sequence[ExercisesTypes]:
        return await self.repository.get_all()
