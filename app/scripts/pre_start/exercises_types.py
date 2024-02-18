import asyncio
import logging

from app import consts
from app.db.session import DB
from app.models import ExercisesTypes
from app.repositories import ExercisesTypesRepository
from app.schemas import CreateExercisesTypeIn

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def create_exercises_types() -> None:
    [exercise.name for exercise in consts.BasicExercisesTypesEnum]

    repository = ExercisesTypesRepository(
        model=ExercisesTypes,
        session_factory=DB().session,
    )

    for exercises_type in consts.ExercisesTypesEnum:
        exercises_type_out = await repository.get_by_type(type=exercises_type)
        if exercises_type_out:
            continue

        await repository.create(schema_in=CreateExercisesTypeIn(type=exercises_type))

        logger.info(
            f"Exercises type created - {consts.EXERCISES_TYPES_DESC[exercises_type]}"
        )


if __name__ == "__main__":
    asyncio.run(create_exercises_types())
