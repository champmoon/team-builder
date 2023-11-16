import asyncio
import logging

from app import consts
from app.db.session import DB
from app.models import WorkoutsStatuses
from app.repositories import WorkoutsStatusesRepository
from app.schemas import CreateWorkoutStatusesIn

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def create_workouts_statuses() -> None:
    repository = WorkoutsStatusesRepository(
        model=WorkoutsStatuses,
        session_factory=DB().session,
    )

    for workout_status in consts.WorkoutsStatusesEnum:
        workout_status_out = await repository.get_by_status(status=workout_status)
        if workout_status_out:
            continue

        await repository.create(
            schema_in=CreateWorkoutStatusesIn(status=workout_status)
        )
        logger.info(
            f"Workout status created - {consts.WORKOUTS_STATUSES_DESC[workout_status]}"
        )


if __name__ == "__main__":
    asyncio.run(create_workouts_statuses())
