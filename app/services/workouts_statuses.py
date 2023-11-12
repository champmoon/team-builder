from typing import Sequence

from app.consts import WorkoutsStatusesEnum
from app.models import WorkoutsStatuses
from app.repositories import WorkoutsStatusesRepository


class WorkoutsStatusesService:
    def __init__(self, repository: WorkoutsStatusesRepository) -> None:
        self.repository = repository

    async def get_by_status(self, status: WorkoutsStatusesEnum) -> WorkoutsStatuses | None:
        return await self.repository.get_by_status(status=status)

    async def get_all(self) -> Sequence[WorkoutsStatuses]:
        return await self.repository.get_all()
