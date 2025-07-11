import logging
from typing import Sequence
from uuid import UUID

from pydantic import ValidationError

from app import consts, schemas
from app.models import Exercises
from app.repositories import ExercisesRepository
from app.schemas.exercises_types import ExercisesTypesOut
from app.schemas.utils import TimeFormat

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

    async def pre_validation(
        self,
        trainer_id: UUID,
        exercises_in: list[
            schemas.CreateBasicExerciseIn | schemas.CreateSupportExerciseIn
        ],
    ) -> None:
        for exercise_in in exercises_in:
            exercise_type_out = await self.exercises_types_service.get_by_type(
                type=exercise_in.type.type,
                trainer_id=trainer_id,
            )
            if not exercise_type_out:
                raise ValueError(f"exercise type - {exercise_in.type} not found")

            if isinstance(exercise_in, schemas.CreateBasicExerciseIn):
                if exercise_type_out.is_basic is False:
                    raise ValueError(
                        f"exercise with type - {exercise_type_out.type} is support, but"
                        " received as basic"
                    )
            elif isinstance(exercise_in, schemas.CreateSupportExerciseIn):
                if exercise_type_out.is_basic is True:
                    raise ValueError(
                        f"exercise with type - {exercise_type_out.type} is basic, but"
                        " received as support"
                    )
            else:
                raise ValueError

    async def create(
        self,
        workout_pool_id: UUID,
        trainer_id: UUID,
        exercises_in: list[
            schemas.CreateBasicExerciseIn | schemas.CreateSupportExerciseIn
        ],
    ) -> None:
        for order, exercise_in in enumerate(exercises_in):
            exercise_type_out = await self.exercises_types_service.get_by_type(
                type=exercise_in.type.type,
                trainer_id=trainer_id,
            )
            if not exercise_type_out:
                raise ExercisesTypesNotFoundException(type=exercise_in.type.type)

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
                assert exercise_out.rest
                exercise_schema = schemas.CreateBasicExerciseIn(
                    type=ExercisesTypesOut(
                        type=exercise_out.type.type,
                        description=exercise_out.type.description,
                        is_basic=exercise_out.type.is_basic,
                    ),
                    reps=exercise_out.reps,
                    sets=exercise_out.sets,
                    rest=TimeFormat(
                        hour=exercise_out.rest["hour"],
                        minute=exercise_out.rest["minute"],
                        second=exercise_out.rest["second"],
                    ),
                )
            except (ValidationError, ValueError, TypeError) as e:
                assert exercise_out.time
                exercise_schema = schemas.CreateSupportExerciseIn(
                    type=ExercisesTypesOut(
                        type=exercise_out.type.type,
                        description=exercise_out.type.description,
                        is_basic=exercise_out.type.is_basic,
                    ),
                    time=TimeFormat(
                        hour=exercise_out.time["hour"],
                        minute=exercise_out.time["minute"],
                        second=exercise_out.time["second"],
                    ),
                )
            exercises_schemas.append(exercise_schema)

        return exercises_schemas
