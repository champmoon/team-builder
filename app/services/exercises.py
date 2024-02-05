from typing import Sequence, cast
from uuid import UUID

from app import consts, schemas
from app.models import Exercises
from app.repositories import ExercisesRepository

from .exercises_types import ExercisesTypesService
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class ExercisesTypesNotFoundException(Exception):
    def __init__(self, type: int) -> None:
        msg = f"Exercise type not found - {type}"
        logger.error(msg)
        super().__init__(msg)


class ExercisesService:
    def __init__(
        self,
        repository: ExercisesRepository,
        exercises_types_service: ExercisesTypesService,
    ) -> None:
        self.repository = repository

        self.exercises_types_service = exercises_types_service

    async def get_all_exercises_by_workout_id(
        self, workout_id: UUID
    ) -> Sequence[Exercises]:
        return await self.repository.get_all_exercises_by_workout_id(
            workout_id=workout_id
        )

    async def create(
        self,
        workout_id: UUID,
        exercises_in: list[
            schemas.CreateBasicExerciseIn | schemas.CreateSupportExerciseIn
        ],
    ) -> list[schemas.BasicExerciseOut | schemas.SupportExerciseOut]:
        exercises_schemas_out: list[
            schemas.BasicExerciseOut | schemas.SupportExerciseOut
        ] = []
        for order, exercise_in in enumerate(exercises_in):
            exercise_type_out = await self.exercises_types_service.get_by_type(
                type=consts.ExercisesTypesEnum(exercise_in.type)
            )
            if not exercise_type_out:
                raise ExercisesTypesNotFoundException(type=exercise_in.type)

            exercise_schema_out: schemas.BasicExerciseOut | schemas.SupportExerciseOut
            if isinstance(exercise_in, schemas.CreateBasicExerciseIn):
                new_schema_in = schemas.CreateExerciseInDB(
                    workout_id=workout_id,
                    type_id=exercise_type_out.id,
                    reps=exercise_in.reps,
                    sets=exercise_in.sets,
                    rest=exercise_in.rest,
                    order=order + 1,
                )
                new_exercise_out = await self.repository.create(schema_in=new_schema_in)
                exercise_schema_out = schemas.BasicExerciseOut(
                    id=new_exercise_out.id,
                    type=consts.BasicExercisesTypesEnum(exercise_type_out.type),
                    reps=exercise_in.reps,
                    sets=exercise_in.sets,
                    rest=exercise_in.rest,
                    order=order + 1,
                )
            else:
                new_schema_in = schemas.CreateExerciseInDB(
                    workout_id=workout_id,
                    type_id=exercise_type_out.id,
                    time=exercise_in.time,
                    order=order + 1,
                )
                new_exercise_out = await self.repository.create(schema_in=new_schema_in)
                exercise_schema_out = schemas.SupportExerciseOut(
                    id=new_exercise_out.id,
                    type=consts.SupportExercisesTypesEnum(exercise_type_out.type),
                    time=exercise_in.time,
                    order=order + 1,
                )

            exercises_schemas_out.append(exercise_schema_out)

        return exercises_schemas_out
