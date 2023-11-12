from uuid import UUID

from app import consts, schemas
from app.models import Exercises
from app.repositories import ExercisesRepository

from .exercises_types import ExercisesTypesService


class ExercisesService:
    def __init__(
        self,
        repository: ExercisesRepository,
        exercises_types_service: ExercisesTypesService,
    ) -> None:
        self.repository = repository

        self.exercises_types_service = exercises_types_service

    async def create(
        self,
        workout_id: UUID,
        type_id: UUID,
        exercise_in: schemas.CreateBasicExerciseIn | schemas.CreateSupportExerciseIn,
    ) -> Exercises:
        match type(exercise_in):
            case schemas.CreateBasicExerciseIn:
                return await self.repository.create(
                    schema_in=schemas.CreateExerciseInDB(
                        workout_id=workout_id,
                        type_id=type_id,
                        reps=exercise_in.reps,
                        sets=exercise_in.sets,
                        rest=exercise_in.rest,
                        order=exercise_in.order,
                    )
                )

            case schemas.CreateSupportExerciseIn:
                return await self.repository.create(
                    schema_in=schemas.CreateExerciseInDB(
                        workout_id=workout_id,
                        type_id=type_id,
                        time=exercise_in.time,
                        order=exercise_in.order,
                    )
                )

            case _:
                raise ValueError(f"create exercise, unexpected class - {exercise_in}")

    async def count_estimated_time(
        self,
        exercises: list[
            schemas.CreateBasicExerciseIn | schemas.CreateSupportExerciseIn
        ],
    ) -> float:
        estimated_time = 0
        for exercise in exercises:

            match type(exercise):
                case schemas.CreateBasicExerciseIn:
                    exercise_type_out = await self.exercises_types_service.get_by_type(
                        type=consts.ExercisesTypesEnum[exercise.type.name]
                    )
                    if exercise_type_out.average_time is None:
                        raise ValueError(
                            "Impossible not average_time in basic exercises types"
                        )

                    full_rest_time = (exercise.sets - 1) * exercise.rest
                    full_execution_time = (
                        exercise.sets * exercise.reps * exercise_type_out.average_time
                    )
                    estimated_time += full_rest_time + full_execution_time

                case schemas.CreateSupportExerciseIn:
                    estimated_time += exercise.time

                case _:
                    raise ValueError(
                        f"count estimated time, unexpected class - {exercise}"
                    )

        return estimated_time
