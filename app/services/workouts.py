from app import schemas
from app.repositories import WorkoutsRepository

from .exercises import ExercisesService

# from .wor


class WorkoutsService:
    def __init__(
        self,
        repository: WorkoutsRepository,
        exercises_service: ExercisesService,
        # sportsmans_workouts_service:
    ) -> None:
        self.repository = repository

        self.exercises_service = exercises_service

    async def create(self, schema_in: schemas.BaseCreateWorkoutIn) -> None:
        match type(schema_in):
            case schemas.CreateWorkoutForSportsmanIn: ...

            case schemas.CreateWorkoutForGroupIn: ...

            case schemas.CreateWorkoutForTeamIn: ...

            case _:
                raise ValueError(f"create workout, unexpected class - {schema_in}")

    async def create_for_sportsman(
        self, schema_in: schemas.CreateWorkoutForSportsmanIn
    ):
        estimated_time = await self.exercises_service.count_estimated_time(
            exercices=schema_in.exercices,
        )

        new_workout_out = await self.repository.create(
            schema_in=schemas.CreateWorkoutInDB(
                date=schema_in.date,
                name=schema_in.name,
                estimated_time=estimated_time,
            )
        )

        new_exercises_out = []
        for exercise_in in schema_in.exercices:
            new_exercises_out.append(
                await self.exercises_service.create(
                    workout_id=new_workout_out.id,
                    exercise_in=exercise_in,
                )
            )

        
