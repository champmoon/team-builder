import logging
from typing import Sequence
from uuid import UUID

from pydantic import ValidationError

from app import consts, schemas
from app.models import Exercises
from app.repositories import ExercisesRepository

from .exercises_types import ExercisesTypesService

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

    async def get_all_exercises_by_workout_pool_id(
        self, workout_pool_id: UUID
    ) -> Sequence[Exercises]:
        return await self.repository.get_all_exercises_by_workout_pool_id(
            workout_pool_id=workout_pool_id
        )

    async def create(
        self,
        workout_pool_id: UUID,
        exercises_in: list[
            schemas.CreateBasicExerciseIn | schemas.CreateSupportExerciseIn
        ],
    ) -> None:
        for order, exercise_in in enumerate(exercises_in):
            exercise_type_out = await self.exercises_types_service.get_by_type(
                type=consts.ExercisesTypesEnum(exercise_in.type)
            )
            if not exercise_type_out:
                raise ExercisesTypesNotFoundException(type=exercise_in.type)

            if isinstance(exercise_in, schemas.CreateBasicExerciseIn):
                new_schema_in = schemas.CreateExerciseInDB(
                    workout_pool_id=workout_pool_id,
                    type_id=exercise_type_out.id,
                    reps=exercise_in.reps,
                    sets=exercise_in.sets,
                    rest=exercise_in.rest,
                    order=order + 1,
                )
            else:
                new_schema_in = schemas.CreateExerciseInDB(
                    workout_pool_id=workout_pool_id,
                    type_id=exercise_type_out.id,
                    time=exercise_in.time,
                    order=order + 1,
                )

            await self.repository.create(schema_in=new_schema_in)

    async def get_schemas_by_orm_models(
        self,
        exercises_out: Sequence[Exercises],
    ) -> list[schemas.CreateBasicExerciseIn | schemas.CreateSupportExerciseIn]:
        exercises_schemas: list[
            schemas.CreateBasicExerciseIn | schemas.CreateSupportExerciseIn
        ] = []
        exercise_schema: schemas.CreateBasicExerciseIn | schemas.CreateSupportExerciseIn
        for exercise_out in exercises_out:
            try:
                exercise_schema = schemas.CreateBasicExerciseIn(
                    type=consts.BasicExercisesTypesEnum(exercise_out.type.type),
                    reps=exercise_out.reps,
                    sets=exercise_out.sets,
                    rest=exercise_out.rest,
                )
            except (ValidationError, ValueError):
                exercise_schema = schemas.CreateSupportExerciseIn(
                    type=consts.SupportExercisesTypesEnum(exercise_out.type.type),
                    time=exercise_out.time,
                )
            exercises_schemas.append(exercise_schema)

        return exercises_schemas
