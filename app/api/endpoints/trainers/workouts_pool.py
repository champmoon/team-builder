import datetime
from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Trainers
from app.models.workouts import Workouts
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.TrainerWorkoutPoolOut,
    status_code=status.HTTP_201_CREATED,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_workout_pool(
    create_workout_in: schemas.CreateWorkoutPoolIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    exercises_service: Services.exercises = Depends(
        Provide[Containers.exercises.service]
    ),
    workouts_pool_service: Services.workouts_pool = Depends(
        Provide[Containers.workouts_pool.service],
    ),
) -> Any:
    try:
        await exercises_service.pre_validation(
            trainer_id=self_trainer.id,
            exercises_in=create_workout_in.exercises,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    new_workout_pool_out = await workouts_pool_service.create(
        schema_in=schemas.CreateWorkoutPoolInDB(
            name=create_workout_in.name,
            trainer_id=self_trainer.id,
            estimated_time=create_workout_in.estimated_time,
        ),
    )

    await exercises_service.create(
        workout_pool_id=new_workout_pool_out.id,
        trainer_id=self_trainer.id,
        exercises_in=create_workout_in.exercises,
    )

    workout_pool_out = await workouts_pool_service.get_by_id(id=new_workout_pool_out.id)
    if not workout_pool_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_no new_workout_pool",
        )

    return workout_pool_out


async def get_workout_pool(
    id: UUID,
    self_trainer: Trainers,
    workouts_pool_service: Services.workouts_pool,
) -> Any:
    workout_pool_out = await workouts_pool_service.get_by_id(id=id)
    if not workout_pool_out or workout_pool_out.trainer_id != self_trainer.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="workout_pool"
        )

    return workout_pool_out


@router(
    response_model=list[schemas.TrainerWorkoutPoolOut] | schemas.TrainerWorkoutPoolOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_workouts_pool(
    id: UUID | None = None,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_pool_service: Services.workouts_pool = Depends(
        Provide[Containers.workouts_pool.service],
    ),
) -> Any:
    if id:
        return await get_workout_pool(
            id=id,
            self_trainer=self_trainer,
            workouts_pool_service=workouts_pool_service,
        )
    return await workouts_pool_service.get_by_trainer_id(trainer_id=self_trainer.id)


@router(
    status_code=status.HTTP_204_NO_CONTENT,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def delete_workout_pool(
    id: UUID,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_pool_service: Services.workouts_pool = Depends(
        Provide[Containers.workouts_pool.service],
    ),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
) -> None:
    workout_pool_out = await workouts_pool_service.get_by_id(id=id)
    if not workout_pool_out or workout_pool_out.trainer_id != self_trainer.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="workout_pool"
        )

    workouts_outs = await workouts_service.get_by_pool_id(pool_id=workout_pool_out.id)
    past_workouts_cnt = 0
    time_now = datetime.timedelta(hours=3) + datetime.datetime.now(
        datetime.UTC
    ).replace(tzinfo=None)
    for workout_out in workouts_outs:
        if time_now > workout_out.date:
            past_workouts_cnt += 1
            # await workouts_service.set_unvisible(id=workout_out.id)
        else:
            await workouts_service.delete(id=workout_out.id)

    if past_workouts_cnt == 0:
        await workouts_pool_service.delete(id=id)
    else:
        await workouts_pool_service.set_unvisible(id=workout_pool_out.id)


@router(
    response_model=schemas.TrainerWorkoutPoolOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def update_workout_pool(
    id: UUID,
    update_workout_pool_in: schemas.UpdateWorkoutPoolIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    workouts_pool_service: Services.workouts_pool = Depends(
        Provide[Containers.workouts_pool.service],
    ),
    exercises_service: Services.exercises = Depends(
        Provide[Containers.exercises.service]
    ),
) -> Any:
    workout_pool_out = await workouts_pool_service.get_by_id(id=id)
    if not workout_pool_out or workout_pool_out.trainer_id != self_trainer.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="workout_pool"
        )

    workouts_outs = await workouts_service.get_by_pool_id(pool_id=workout_pool_out.id)
    past_workouts_cnt = 0
    future_workouts_outs: list[Workouts] = []
    time_now = datetime.timedelta(hours=3) + datetime.datetime.now(
        datetime.UTC
    ).replace(tzinfo=None)
    for workout_out in workouts_outs:
        if time_now > workout_out.date:
            past_workouts_cnt += 1
        else:
            future_workouts_outs.append(workout_out)
    # if len(future_workouts_outs) == 0:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="workout")

    new_workout_pool_out = await workouts_pool_service.create(
        schema_in=schemas.CreateWorkoutPoolInDB(
            name=(update_workout_pool_in.name or workout_pool_out.name),
            trainer_id=self_trainer.id,
            estimated_time=(
                update_workout_pool_in.estimated_time or workout_pool_out.estimated_time
            ),
        )
    )

    new_exercises_in: list[
        schemas.CreateBasicExerciseIn | schemas.CreateSupportExerciseIn
    ]
    if update_workout_pool_in.exercises is not None:
        new_exercises_in = update_workout_pool_in.exercises
    else:
        new_exercises_in = await exercises_service.get_schemas_by_orm_models(
            exercises_out=workout_pool_out.exercises
        )
    await exercises_service.create(
        workout_pool_id=new_workout_pool_out.id,
        trainer_id=self_trainer.id,
        exercises_in=new_exercises_in,
    )

    for future_workout_out in future_workouts_outs:
        await workouts_service.reassign(
            id=future_workout_out.id,
            workout_pool_id=new_workout_pool_out.id,
        )

    if past_workouts_cnt == 0:
        await workouts_pool_service.delete(id=workout_pool_out.id)
    else:
        await workouts_pool_service.set_unvisible(id=workout_pool_out.id)

    return await workouts_pool_service.get_by_id(id=new_workout_pool_out.id)
