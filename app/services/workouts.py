from uuid import UUID
from app import schemas
from app.models.exercises import Exercises
from app.repositories import WorkoutsRepository
from app import consts
from .exercises import ExercisesService
from .sportsmans_workouts import SportsmansWorkoutsService
from .trainers_workouts import TrainersWorkoutsService
from .workouts_statuses import WorkoutsStatusesService
from .exercises_types import ExercisesTypesService

class WorkoutsService:
    def __init__(
        self,
        repository: WorkoutsRepository,
        exercises_service: ExercisesService,
        sportsmans_workouts_service: SportsmansWorkoutsService,
        trainers_workouts_service: TrainersWorkoutsService,
        workouts_statuses_service: WorkoutsStatusesService,
        exercises_types_service: ExercisesTypesService,
    ) -> None:
        self.repository = repository

        self.exercises_service = exercises_service
        self.sportsmans_workouts_service = sportsmans_workouts_service
        self.trainers_workouts_service = trainers_workouts_service
        self.workouts_statuses_service = workouts_statuses_service
        self.exercises_types_service = exercises_types_service

    async def create(self, trainer_id: UUID, schema_in: schemas.BaseCreateWorkoutIn) -> None:
        match type(schema_in):
            case schemas.CreateWorkoutForSportsmanIn:
                return await self.create_for_sportsman(
                    trainer_id=trainer_id,
                    schema_in=schema_in
                )

            case schemas.CreateWorkoutForGroupIn: ...

            case schemas.CreateWorkoutForTeamIn: ...

            case _:
                raise ValueError(f"create workout, unexpected class - {schema_in}")

    async def create_for_sportsman(
        self, trainer_id: UUID, schema_in: schemas.CreateWorkoutForSportsmanIn
    ) -> schemas.TrainerWorkoutOut:
        estimated_time = await self.exercises_service.count_estimated_time(
            exercises=schema_in.exercises,
        )

        new_workout_out = await self.repository.create(
            schema_in=schemas.CreateWorkoutInDB(
                date=schema_in.date,
                name=schema_in.name,
                estimated_time=estimated_time,
            )
        )

        new_exercises_schemas: list[Exercises] = []
        for exercise_in in schema_in.exercises:
            type_out = await self.exercises_types_service.get_by_type(
                type=consts.ExercisesTypesEnum[exercise_in.type.name]
            )
            
            new_exercises_out = await self.exercises_service.create(
                    workout_id=new_workout_out.id,
                    type_id=type_out.id,
                    exercise_in=exercise_in,
                )
            
            new_exercises_schemas.append(
                schemas.ExerciseOut(
                    type=schemas.ExercisesTypesOut(
                        type=type_out.type,
                        average_time=type_out.average_time
                    ),
                    reps=new_exercises_out.reps,
                    sets=new_exercises_out.sets,
                    rest=new_exercises_out.rest,
                    time=new_exercises_out.time,
                    order=new_exercises_out.order,
                )
            )

        status_out = await self.workouts_statuses_service.get_by_status(
            status=consts.WorkoutsStatusesEnum.PLANNED
        )
        assert status_out is not None

        await self.sportsmans_workouts_service.create(
            schema_in=schemas.CreateSportsmansWorkoutIn(
                sportsman_id=schema_in.sportsman_id,
                workout_id=new_workout_out.id,
                status_id=status_out.id,
            )
        )

        await self.trainers_workouts_service.create(
            schema_in=schemas.CreateTrainerWorkoutIn(
                trainer_id=trainer_id,
                workout_id=new_workout_out.id,
                status_id=status_out.id
            )
        )

        return schemas.TrainerWorkoutOut(
            trainer_id=trainer_id,
            workout_id=new_workout_out.id,
            name=new_workout_out.name,
            estimated_time=estimated_time,
            # status=consts.WorkoutsStatusesEnum(status_out.status),
            status=schemas.WorkoutsStatusesOut(
                status=status_out.status,
                description=consts.WORKOUTS_STATUSES_DESC[status_out.status],
            ),
            date=new_workout_out.date,
            created_at=new_workout_out.created_at,
            exercises=new_exercises_schemas
        )
