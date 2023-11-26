from typing import Sequence
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
    ) -> list[schemas.ExerciseOut]:
        exercises_schemas: list[schemas.ExerciseOut] = []
        for order, exercise_in in enumerate(exercises_in):
            exercise_type_out = await self.exercises_types_service.get_by_type(
                type=consts.ExercisesTypesEnum[exercise_in.type.name]
            )
            if not exercise_type_out:
                raise ValueError(
                    f"Not found exercise_type_out with type - {exercise_in.type}"
                )

            match type(exercise_in):
                case schemas.CreateBasicExerciseIn:
                    new_exercise_out = await self.repository.create(
                        schema_in=schemas.CreateExerciseInDB(
                            workout_id=workout_id,
                            type_id=exercise_type_out.id,
                            reps=exercise_in.reps,  # type: ignore
                            sets=exercise_in.sets,  # type: ignore
                            rest=exercise_in.rest,  # type: ignore
                            order=order + 1,
                        )
                    )

                case schemas.CreateSupportExerciseIn:
                    new_exercise_out = await self.repository.create(
                        schema_in=schemas.CreateExerciseInDB(
                            workout_id=workout_id,
                            type_id=exercise_type_out.id,
                            time=exercise_in.time,  # type: ignore
                            order=order + 1,
                        )
                    )

                case _:
                    raise ValueError(
                        f"create exercise, unexpected class - {exercise_in}"
                    )

            exercises_schemas.append(
                schemas.ExerciseOut(
                    type=schemas.ExercisesTypesOut(
                        type=exercise_type_out.type,
                    ),
                    reps=new_exercise_out.reps,
                    sets=new_exercise_out.sets,
                    rest=new_exercise_out.rest,
                    time=new_exercise_out.time,
                    order=order + 1,
                )
            )

        return exercises_schemas

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
                    if exercise_type_out.average_time is None:  # type: ignore
                        raise ValueError(
                            "Impossible not average_time in basic exercises types"
                        )

                    full_rest_time = (exercise.sets - 1) * exercise.rest  # type: ignore # noqa
                    full_execution_time = exercise.sets * (  # type: ignore
                        exercise.reps * exercise_type_out.average_time  # type: ignore
                    )
                    estimated_time += full_rest_time + full_execution_time  # type: ignore # noqa

                case schemas.CreateSupportExerciseIn:
                    estimated_time += exercise.time  # type: ignore

                case _:
                    raise ValueError(
                        f"count estimated time, unexpected class - {exercise}"
                    )

        return estimated_time
