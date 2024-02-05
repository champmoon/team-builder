from typing import Sequence

from app.consts import WorkoutsStatusesEnum
from app.models import WorkoutsStatuses

from app.repositories import WorkoutsStatusesRepository
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class WorkoutsStatusesNotFoundException(Exception):
    def __init__(self, status: int) -> None:
        msg = f"Workout status not found - {status}"
        logger.error(msg)
        super().__init__(msg)


class WorkoutsStatusesService:
    def __init__(self, repository: WorkoutsStatusesRepository) -> None:
        self.repository = repository

    async def get_by_status(self, status: WorkoutsStatusesEnum) -> WorkoutsStatuses:
        workout_status_out = await self.repository.get_by_status(status=status)
        if not workout_status_out:
            raise WorkoutsStatusesNotFoundException(status=status)
        return workout_status_out

    async def get_all(self) -> Sequence[WorkoutsStatuses]:
        return await self.repository.get_all()
