from uuid import UUID

from dependency_injector.wiring import Provide, inject

from app import schemas
from app.containers import Containers
from app.services import Services


@inject
async def start_workout(
    workout_id: UUID,
    sportsmans_workouts_service: Services.sportsmans_workouts = Provide[
        Containers.sportsmans_workouts.service
    ],
    trainers_workouts_service: Services.trainers_workouts = Provide[
        Containers.trainers_workouts.service
    ],
) -> None:
    sportsmans_workouts_out = await sportsmans_workouts_service.get_all_by_workout_id(
        workout_id=workout_id
    )
    for sportsman_workout_out in sportsmans_workouts_out:
        await sportsmans_workouts_service.active(
            schema_in=schemas.UpdateSportsmansWorkoutIn(
                sportsman_id=sportsman_workout_out.sportsman_id,
                workout_id=workout_id,
            )
        )
    trainers_workouts_out = await trainers_workouts_service.get_all_by_workout_id(
        workout_id=workout_id
    )
    for trainer_workout_out in trainers_workouts_out:
        await trainers_workouts_service.active(
            schema_in=schemas.UpdateTrainerWorkoutIn(
                trainer_id=trainer_workout_out.trainer_id,
                workout_id=workout_id,
            )
        )


@inject
async def skip_workout_sportsman(
    workout_id: UUID,
    sportsman_id: UUID,
    sportsmans_workouts_service: Services.sportsmans_workouts = Provide[
        Containers.sportsmans_workouts.service
    ],
) -> None:
    await sportsmans_workouts_service.skipped(
        schema_in=schemas.UpdateSportsmansWorkoutIn(
            sportsman_id=sportsman_id,
            workout_id=workout_id,
        )
    )


@inject
async def skip_workout_trainer(
    workout_id: UUID,
    trainer_id: UUID,
    trainer_workouts_service: Services.trainers_workouts = Provide[
        Containers.trainers_workouts.service
    ],
) -> None:
    await trainer_workouts_service.skipped(
        schema_in=schemas.UpdateTrainerWorkoutIn(
            trainer_id=trainer_id,
            workout_id=workout_id,
        )
    )
