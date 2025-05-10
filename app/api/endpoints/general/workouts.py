from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from pydantic import NaiveDatetime

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Trainers
from app.models.sportsmans import Sportsmans
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=list[
        schemas.TrainerSportsmanWorkoutOut
        | schemas.TrainerGroupWorkoutOut
        | schemas.TrainerTeamWorkoutOut
    ]
    | schemas.TrainerSportsmanWorkoutOut
    | schemas.TrainerGroupWorkoutOut
    | schemas.TrainerTeamWorkoutOut
    | list[
        schemas.SportsmansSportsmanWorkoutOut
        | schemas.SportsmansGroupWorkoutOut
        | schemas.SportsmansTeamWorkoutOut
    ]
    | schemas.SportsmansSportsmanWorkoutOut
    | schemas.SportsmansGroupWorkoutOut
    | schemas.SportsmansTeamWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER, UsersTypes.SPORTSMAN])
@inject
async def get_workouts(
    id: UUID | None = None,
    offset: int = 0,
    limit: int = 100,
    start_date: NaiveDatetime | None = None,
    end_date: NaiveDatetime | None = None,
    self_user: Trainers | Sportsmans = Depends(deps.self_user),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
) -> Any:
    if isinstance(self_user, Trainers):
        if id:
            return await get_workout_for_trainer(
                id=id,
                self_trainer=self_user,
                workouts_service=workouts_service,
                trainers_workouts_service=trainers_workouts_service,
                tgs_workouts_service=tgs_workouts_service,
            )
        return await get_workouts_for_trainer(
            self_trainer=self_user,
            workouts_service=workouts_service,
            trainers_workouts_service=trainers_workouts_service,
            tgs_workouts_service=tgs_workouts_service,
            offset=offset,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
        )
    if id:
        return await get_workout_for_sportsman(
            id=id,
            self_sportsman=self_user,
            workouts_service=workouts_service,
            sportsmans_workouts_service=sportsmans_workouts_service,
            tgs_workouts_service=tgs_workouts_service,
        )
    return await get_workouts_for_sportsman(
        self_sportsman=self_user,
        workouts_service=workouts_service,
        sportsmans_workouts_service=sportsmans_workouts_service,
        tgs_workouts_service=tgs_workouts_service,
        offset=offset,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )


async def get_workouts_for_trainer(
    self_trainer: Trainers,
    workouts_service: Services.workouts,
    trainers_workouts_service: Services.trainers_workouts,
    tgs_workouts_service: Services.tgs_workouts,
    offset: int,
    limit: int,
    start_date: NaiveDatetime | None = None,
    end_date: NaiveDatetime | None = None,
) -> list[
    schemas.TrainerSportsmanWorkoutOut
    | schemas.TrainerGroupWorkoutOut
    | schemas.TrainerTeamWorkoutOut
]:
    trainers_workouts_out = await trainers_workouts_service.get_all_by_trainer_id(
        trainer_id=self_trainer.id,
        offset=offset,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )
    workouts: list[
        schemas.TrainerSportsmanWorkoutOut
        | schemas.TrainerGroupWorkoutOut
        | schemas.TrainerTeamWorkoutOut
    ] = []
    for trainer_workout_out in trainers_workouts_out:
        workout_out = await workouts_service.get_by_id(
            id=trainer_workout_out.workout_id
        )
        if not workout_out:
            continue
            # raise HTTPException(
            #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     detail="_trainer_workout not in workout db",
            # )

        base_workouts_schemas = schemas.TrainerWorkoutOut(
            id=workout_out.id,
            repeat_id=workout_out.repeat_id,
            name=workout_out.workout_pool.name,
            estimated_time=workout_out.workout_pool.estimated_time,
            # status=schemas.WorkoutsStatusesOut(
            #     status=consts.WorkoutsStatusesEnum(trainer_workout_out.status.status),
            #     description=consts.WORKOUTS_STATUSES_DESC[
            #         consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
            #     ],
            # ),
            date=workout_out.date,
            created_at=workout_out.workout_pool.created_at,
            exercises=workout_out.workout_pool.exercises,
            rest_time=workout_out.rest_time,
            price=workout_out.price,
            comment=workout_out.comment,
            goal=workout_out.goal,
        )

        tgs_workouts_out = await tgs_workouts_service.get_by_workout_id(
            workout_id=trainer_workout_out.workout_id
        )
        if not tgs_workouts_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_workout not found in tgs",
            )

        workout_schema: (
            schemas.TrainerSportsmanWorkoutOut
            | schemas.TrainerGroupWorkoutOut
            | schemas.TrainerTeamWorkoutOut
        )
        team_id = tgs_workouts_out.team_id
        group_id = tgs_workouts_out.group_id
        sportsman_id = tgs_workouts_out.sportsman_id
        if team_id:
            workout_schema = schemas.TrainerTeamWorkoutOut(
                **base_workouts_schemas.model_dump(),
                team_id=team_id,
            )
        elif group_id:
            workout_schema = schemas.TrainerGroupWorkoutOut(
                **base_workouts_schemas.model_dump(),
                group_id=group_id,
            )
        elif sportsman_id:
            workout_schema = schemas.TrainerSportsmanWorkoutOut(
                **base_workouts_schemas.model_dump(),
                sportsman_id=sportsman_id,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_tgs all none ids",
            )

        workouts.append(workout_schema)

    return workouts


async def get_workout_for_trainer(
    id: UUID,
    self_trainer: Trainers,
    workouts_service: Services.workouts,
    trainers_workouts_service: Services.trainers_workouts,
    tgs_workouts_service: Services.tgs_workouts,
) -> (
    schemas.TrainerSportsmanWorkoutOut
    | schemas.TrainerGroupWorkoutOut
    | schemas.TrainerTeamWorkoutOut
):
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out or workout_out.workout_pool.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    trainer_workout_out = await trainers_workouts_service.get_by(
        workout_id=workout_out.id,
        trainer_id=self_trainer.id,
    )
    if not trainer_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    base_workouts_schemas = schemas.TrainerWorkoutOut(
        id=workout_out.id,
        repeat_id=workout_out.repeat_id,
        name=workout_out.workout_pool.name,
        estimated_time=workout_out.workout_pool.estimated_time,
        # status=schemas.WorkoutsStatusesOut(
        #     status=consts.WorkoutsStatusesEnum(trainer_workout_out.status.status),
        #     description=consts.WORKOUTS_STATUSES_DESC[
        #         consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
        #     ],
        # ),
        date=workout_out.date,
        created_at=workout_out.workout_pool.created_at,
        exercises=workout_out.workout_pool.exercises,
        rest_time=workout_out.rest_time,
        price=workout_out.price,
        comment=workout_out.comment,
        goal=workout_out.goal,
    )

    tgs_workouts_out = await tgs_workouts_service.get_by_workout_id(
        workout_id=trainer_workout_out.workout_id
    )
    if not tgs_workouts_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_workout not found in tgs",
        )

    workout_schema: (
        schemas.TrainerSportsmanWorkoutOut
        | schemas.TrainerGroupWorkoutOut
        | schemas.TrainerTeamWorkoutOut
    )
    team_id = tgs_workouts_out.team_id
    group_id = tgs_workouts_out.group_id
    sportsman_id = tgs_workouts_out.sportsman_id
    if team_id:
        workout_schema = schemas.TrainerTeamWorkoutOut(
            **base_workouts_schemas.model_dump(),
            team_id=team_id,
        )
    elif group_id:
        workout_schema = schemas.TrainerGroupWorkoutOut(
            **base_workouts_schemas.model_dump(),
            group_id=group_id,
        )
    elif sportsman_id:
        workout_schema = schemas.TrainerSportsmanWorkoutOut(
            **base_workouts_schemas.model_dump(),
            sportsman_id=sportsman_id,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_tgs all none ids",
        )

    return workout_schema


async def get_workouts_for_sportsman(
    self_sportsman: Sportsmans,
    workouts_service: Services.workouts,
    sportsmans_workouts_service: Services.sportsmans_workouts,
    tgs_workouts_service: Services.tgs_workouts,
    offset: int,
    limit: int,
    start_date: NaiveDatetime | None = None,
    end_date: NaiveDatetime | None = None,
) -> list[
    schemas.SportsmansSportsmanWorkoutOut
    | schemas.SportsmansGroupWorkoutOut
    | schemas.SportsmansTeamWorkoutOut
]:
    sportsmans_workouts_out = await sportsmans_workouts_service.get_all_by_sportsman_id(
        sportsman_id=self_sportsman.id,
        offset=offset,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
    )
    workouts: list[
        schemas.SportsmansSportsmanWorkoutOut
        | schemas.SportsmansGroupWorkoutOut
        | schemas.SportsmansTeamWorkoutOut
    ] = []
    for sportsmans_workout_out in sportsmans_workouts_out:
        workout_out = await workouts_service.get_by_id(
            id=sportsmans_workout_out.workout_id
        )
        if not workout_out:
            continue
            # raise HTTPException(
            #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     detail="_trainer_workout not in workout db",
            # )

        base_workouts_schemas = schemas.SportsmansWorkoutOut(
            id=workout_out.id,
            name=workout_out.workout_pool.name,
            estimated_time=workout_out.workout_pool.estimated_time,
            # status=schemas.WorkoutsStatusesOut(
            #     status=consts.WorkoutsStatusesEnum(
            #         sportsmans_workout_out.status.status
            #     ),
            #     description=consts.WORKOUTS_STATUSES_DESC[
            #         consts.WorkoutsStatusesEnum(sportsmans_workout_out.status.status)
            #     ],
            # ),
            is_paid=sportsmans_workout_out.is_paid,
            is_attend=sportsmans_workout_out.is_attend,
            date=workout_out.date,
            created_at=workout_out.workout_pool.created_at,
            exercises=workout_out.workout_pool.exercises,
            rest_time=workout_out.rest_time,
            price=workout_out.price,
            comment=workout_out.comment,
            goal=workout_out.goal,
            repeat_id=workout_out.repeat_id,
            sportsman_id=sportsmans_workout_out.sportsman_id,
        )

        tgs_workouts_out = await tgs_workouts_service.get_by_workout_id(
            workout_id=sportsmans_workout_out.workout_id
        )
        if not tgs_workouts_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_workout not found in tgs",
            )

        workout_schema: (
            schemas.SportsmansSportsmanWorkoutOut
            | schemas.SportsmansGroupWorkoutOut
            | schemas.SportsmansTeamWorkoutOut
        )
        team_id = tgs_workouts_out.team_id
        group_id = tgs_workouts_out.group_id
        sportsman_id = tgs_workouts_out.sportsman_id
        if team_id:
            workout_schema = schemas.SportsmansTeamWorkoutOut(
                **base_workouts_schemas.model_dump(),
                team_id=team_id,
            )
        elif group_id:
            workout_schema = schemas.SportsmansGroupWorkoutOut(
                **base_workouts_schemas.model_dump(),
                group_id=group_id,
            )
        elif sportsman_id:
            workout_schema = schemas.SportsmansSportsmanWorkoutOut(
                **base_workouts_schemas.model_dump(),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_tgs all none ids",
            )

        workouts.append(workout_schema)

    return workouts


async def get_workout_for_sportsman(
    id: UUID,
    self_sportsman: Sportsmans,
    workouts_service: Services.workouts,
    sportsmans_workouts_service: Services.sportsmans_workouts,
    tgs_workouts_service: Services.tgs_workouts,
) -> (
    schemas.SportsmansSportsmanWorkoutOut
    | schemas.SportsmansGroupWorkoutOut
    | schemas.SportsmansTeamWorkoutOut
):
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    sportsman_workout_out = await sportsmans_workouts_service.get_by(
        workout_id=workout_out.id, sportsman_id=self_sportsman.id
    )
    if not sportsman_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    base_workouts_schemas = schemas.SportsmansWorkoutOut(
        id=workout_out.id,
        name=workout_out.workout_pool.name,
        estimated_time=workout_out.workout_pool.estimated_time,
        # status=schemas.WorkoutsStatusesOut(
        #     status=consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status),
        #     description=consts.WORKOUTS_STATUSES_DESC[
        #         consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status)
        #     ],
        # ),
        is_paid=sportsman_workout_out.is_paid,
        is_attend=sportsman_workout_out.is_attend,
        date=workout_out.date,
        created_at=workout_out.workout_pool.created_at,
        exercises=workout_out.workout_pool.exercises,
        rest_time=workout_out.rest_time,
        price=workout_out.price,
        comment=workout_out.comment,
        goal=workout_out.goal,
        repeat_id=workout_out.repeat_id,
        sportsman_id=sportsman_workout_out.sportsman_id,
    )

    tgs_workouts_out = await tgs_workouts_service.get_by_workout_id(
        workout_id=sportsman_workout_out.workout_id
    )
    if not tgs_workouts_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_workout not found in tgs",
        )

    workout_schema: (
        schemas.SportsmansSportsmanWorkoutOut
        | schemas.SportsmansGroupWorkoutOut
        | schemas.SportsmansTeamWorkoutOut
    )
    team_id = tgs_workouts_out.team_id
    group_id = tgs_workouts_out.group_id
    sportsman_id = tgs_workouts_out.sportsman_id
    if team_id:
        workout_schema = schemas.SportsmansTeamWorkoutOut(
            **base_workouts_schemas.model_dump(),
            team_id=team_id,
        )
    elif group_id:
        workout_schema = schemas.SportsmansGroupWorkoutOut(
            **base_workouts_schemas.model_dump(),
            group_id=group_id,
        )
    elif sportsman_id:
        workout_schema = schemas.SportsmansSportsmanWorkoutOut(
            **base_workouts_schemas.model_dump(),
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_tgs all none ids",
        )

    return workout_schema
