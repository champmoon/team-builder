import asyncio
import logging

from app.consts import EXERCISES_TYPES_DESC, ExercisesTypesEnum
from app.db.session import DB
from app.models import ExercisesTypes
from app.repositories import ExercisesTypesRepository
from app.schemas import CreateExercisesTypeIn

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def create_exercises_types() -> None:
    repository = ExercisesTypesRepository(
        model=ExercisesTypes,
        session_factory=DB().session,
    )

    for exercises_type in ExercisesTypesEnum:
        exercises_type_out = await repository.get_by_type(type=exercises_type)
        if not exercises_type_out:
            await repository.create(
                schema_in=CreateExercisesTypeIn(
                    type=exercises_type,
                )
            )
            logger.info(
                f"Exercises type created - {EXERCISES_TYPES_DESC[exercises_type]}"
            )


if __name__ == "__main__":
    asyncio.run(create_exercises_types())
