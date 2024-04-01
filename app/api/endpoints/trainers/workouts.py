import datetime
from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from pydantic import EmailStr, NaiveDatetime

from app import consts, schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Trainers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_201_CREATED,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_workout_for_sportsman(
    create_workout_in: schemas.CreateWorkoutForSportsmanIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    workouts_pool_service: Services.workouts_pool = Depends(
        Provide[Containers.workouts_pool.service],
    ),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    workouts_statuses_service: Services.workouts_statuses = Depends(
        Provide[Containers.workouts_statuses.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> Any:
    workout_pool_out = await workouts_pool_service.get_by_id(
        id=create_workout_in.workout_pool_id
    )
    if not workout_pool_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="workout_pool"
        )

    sportsman_email = create_workout_in.sportsman_email

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="_team must exist"
        )

    sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
    if not sportsman_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

    if sportsman_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

    new_workout_out = await workouts_service.create(
        schema_in=schemas.CreateWorkoutInDB(
            workout_pool_id=create_workout_in.workout_pool_id,
            date=create_workout_in.date,
            rest_time=create_workout_in.rest_time,
            stress_questionnaire_time=create_workout_in.stress_questionnaire_time,
        ),
    )

    workout_status_out = await workouts_statuses_service.get_by_status(
        status=consts.WorkoutsStatusesEnum.PLANNED
    )

    await sportsmans_workouts_service.create(
        schema_in=schemas.CreateSportsmansWorkoutIn(
            sportsman_id=sportsman_out.id,
            workout_id=new_workout_out.id,
            status_id=workout_status_out.id,
        )
    )

    await trainers_workouts_service.create(
        schema_in=schemas.CreateTrainerWorkoutIn(
            trainer_id=self_trainer.id,
            workout_id=new_workout_out.id,
            status_id=workout_status_out.id,
        )
    )

    await tgs_workouts_service.create(
        schema_in=schemas.CreateTGSWorkoutIn(
            sportsman_id=sportsman_out.id,
            workout_id=new_workout_out.id,
        )
    )

    return schemas.TrainerWorkoutOut(
        id=new_workout_out.id,
        name=new_workout_out.workout_pool.name,
        estimated_time=new_workout_out.workout_pool.estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=consts.WorkoutsStatusesEnum(workout_status_out.status),
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(workout_status_out.status)
            ],
        ),
        date=new_workout_out.date,
        created_at=new_workout_out.workout_pool.created_at,
        exercises=new_workout_out.workout_pool.exercises,
        rest_time=new_workout_out.rest_time,
        stress_questionnaire_time=new_workout_out.stress_questionnaire_time,
    )


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_201_CREATED,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_workout_for_group(
    create_workout_in: schemas.CreateWorkoutForGroupIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
    workouts_pool_service: Services.workouts_pool = Depends(
        Provide[Containers.workouts_pool.service],
    ),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    workouts_statuses_service: Services.workouts_statuses = Depends(
        Provide[Containers.workouts_statuses.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> Any:
    workout_pool_out = await workouts_pool_service.get_by_id(
        id=create_workout_in.workout_pool_id
    )
    if not workout_pool_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="workout_pool"
        )

    group_id = create_workout_in.group_id
    group_out = await groups_service.get_by_id(id=group_id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group")

    sportsmans_out = await sportsmans_groups_service.get_all_sportsmans_by_group_id(
        group_id=group_id
    )
    if len(sportsmans_out) == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="group")

    new_workout_out = await workouts_service.create(
        schema_in=schemas.CreateWorkoutInDB(
            workout_pool_id=create_workout_in.workout_pool_id,
            date=create_workout_in.date,
            rest_time=create_workout_in.rest_time,
            stress_questionnaire_time=create_workout_in.stress_questionnaire_time,
        ),
    )

    workout_status_out = await workouts_statuses_service.get_by_status(
        status=consts.WorkoutsStatusesEnum.PLANNED
    )

    for sportsman_out in sportsmans_out:
        await sportsmans_workouts_service.create(
            schema_in=schemas.CreateSportsmansWorkoutIn(
                sportsman_id=sportsman_out.sportsman_id,
                workout_id=new_workout_out.id,
                status_id=workout_status_out.id,
            )
        )

    await trainers_workouts_service.create(
        schema_in=schemas.CreateTrainerWorkoutIn(
            trainer_id=self_trainer.id,
            workout_id=new_workout_out.id,
            status_id=workout_status_out.id,
        )
    )

    await tgs_workouts_service.create(
        schema_in=schemas.CreateTGSWorkoutIn(
            group_id=group_id,
            workout_id=new_workout_out.id,
        )
    )

    return schemas.TrainerWorkoutOut(
        id=new_workout_out.id,
        name=new_workout_out.workout_pool.name,
        estimated_time=new_workout_out.workout_pool.estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=consts.WorkoutsStatusesEnum(workout_status_out.status),
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(workout_status_out.status)
            ],
        ),
        date=new_workout_out.date,
        created_at=new_workout_out.workout_pool.created_at,
        exercises=new_workout_out.workout_pool.exercises,
        rest_time=new_workout_out.rest_time,
        stress_questionnaire_time=new_workout_out.stress_questionnaire_time,
    )


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_201_CREATED,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_workout_for_team(
    create_workout_in: schemas.CreateWorkoutForTeamIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_pool_service: Services.workouts_pool = Depends(
        Provide[Containers.workouts_pool.service],
    ),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    workouts_statuses_service: Services.workouts_statuses = Depends(
        Provide[Containers.workouts_statuses.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
) -> Any:
    workout_pool_out = await workouts_pool_service.get_by_id(
        id=create_workout_in.workout_pool_id
    )
    if not workout_pool_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="workout_pool"
        )

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="_team must exist"
        )

    sportsmans_out = await sportsmans_service.get_by_team_id(team_id=team_out.id)
    if len(sportsmans_out) == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="team")

    new_workout_out = await workouts_service.create(
        schema_in=schemas.CreateWorkoutInDB(
            workout_pool_id=create_workout_in.workout_pool_id,
            date=create_workout_in.date,
            rest_time=create_workout_in.rest_time,
            stress_questionnaire_time=create_workout_in.stress_questionnaire_time,
        ),
    )

    workout_status_out = await workouts_statuses_service.get_by_status(
        status=consts.WorkoutsStatusesEnum.PLANNED
    )

    for sportsman_out in sportsmans_out:
        await sportsmans_workouts_service.create(
            schema_in=schemas.CreateSportsmansWorkoutIn(
                sportsman_id=sportsman_out.id,
                workout_id=new_workout_out.id,
                status_id=workout_status_out.id,
            )
        )

    await trainers_workouts_service.create(
        schema_in=schemas.CreateTrainerWorkoutIn(
            trainer_id=self_trainer.id,
            workout_id=new_workout_out.id,
            status_id=workout_status_out.id,
        )
    )

    await tgs_workouts_service.create(
        schema_in=schemas.CreateTGSWorkoutIn(
            team_id=team_out.id,
            workout_id=new_workout_out.id,
        )
    )

    return schemas.TrainerWorkoutOut(
        id=new_workout_out.id,
        name=new_workout_out.workout_pool.name,
        estimated_time=new_workout_out.workout_pool.estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=consts.WorkoutsStatusesEnum(workout_status_out.status),
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(workout_status_out.status)
            ],
        ),
        date=new_workout_out.date,
        created_at=new_workout_out.workout_pool.created_at,
        exercises=new_workout_out.workout_pool.exercises,
        rest_time=new_workout_out.rest_time,
        stress_questionnaire_time=new_workout_out.stress_questionnaire_time,
    )


@router(
    response_model=list[
        schemas.TrainerSportsmanWorkoutOut
        | schemas.TrainerGroupWorkoutOut
        | schemas.TrainerTeamWorkoutOut
    ]
    | schemas.TrainerSportsmanWorkoutOut
    | schemas.TrainerGroupWorkoutOut
    | schemas.TrainerTeamWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_workouts(
    id: UUID | None = None,
    offset: int = 0,
    limit: int = 100,
    start_date: NaiveDatetime | None = None,
    end_date: NaiveDatetime | None = None,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> Any:
    if id:
        return await get_workout(
            id=id,
            self_trainer=self_trainer,
            workouts_service=workouts_service,
            trainers_workouts_service=trainers_workouts_service,
            tgs_workouts_service=tgs_workouts_service,
        )

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
            name=workout_out.workout_pool.name,
            estimated_time=workout_out.workout_pool.estimated_time,
            status=schemas.WorkoutsStatusesOut(
                status=consts.WorkoutsStatusesEnum(trainer_workout_out.status.status),
                description=consts.WORKOUTS_STATUSES_DESC[
                    consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
                ],
            ),
            date=workout_out.date,
            created_at=workout_out.workout_pool.created_at,
            exercises=workout_out.workout_pool.exercises,
            rest_time=workout_out.rest_time,
            stress_questionnaire_time=workout_out.stress_questionnaire_time,
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


async def get_workout(
    id: UUID,
    self_trainer: Trainers,
    workouts_service: Services.workouts,
    trainers_workouts_service: Services.trainers_workouts,
    tgs_workouts_service: Services.tgs_workouts,
) -> Any:
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
        name=workout_out.workout_pool.name,
        estimated_time=workout_out.workout_pool.estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=consts.WorkoutsStatusesEnum(trainer_workout_out.status.status),
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
            ],
        ),
        date=workout_out.date,
        created_at=workout_out.workout_pool.created_at,
        exercises=workout_out.workout_pool.exercises,
        rest_time=workout_out.rest_time,
        stress_questionnaire_time=workout_out.stress_questionnaire_time,
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


@router(
    response_model=list[
        schemas.TrainerSportsmanWorkoutOut
        | schemas.TrainerGroupWorkoutOut
        | schemas.TrainerTeamWorkoutOut
    ],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_workouts_by_pool_id(
    id: UUID,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    workouts_pool_service: Services.workouts_pool = Depends(
        Provide[Containers.workouts_pool.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> Any:
    workout_pool_out = await workouts_pool_service.get_by_id(id=id)
    if not workout_pool_out or workout_pool_out.trainer_id != self_trainer.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="workout_pool"
        )
    workouts_outs = await workouts_service.get_by_pool_id(pool_id=workout_pool_out.id)
    workouts: list[
        schemas.TrainerSportsmanWorkoutOut
        | schemas.TrainerGroupWorkoutOut
        | schemas.TrainerTeamWorkoutOut
    ] = []
    for workout_out in workouts_outs:
        trainer_workout_out = await trainers_workouts_service.get_by(
            workout_id=workout_out.id,
            trainer_id=self_trainer.id,
        )
        if not trainer_workout_out:
            # continue
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_trainer_workout not in workout db",
            )

        base_workouts_schemas = schemas.TrainerWorkoutOut(
            id=workout_out.id,
            name=workout_out.workout_pool.name,
            estimated_time=workout_out.workout_pool.estimated_time,
            status=schemas.WorkoutsStatusesOut(
                status=consts.WorkoutsStatusesEnum(trainer_workout_out.status.status),
                description=consts.WORKOUTS_STATUSES_DESC[
                    consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
                ],
            ),
            date=workout_out.date,
            created_at=workout_out.workout_pool.created_at,
            exercises=workout_out.workout_pool.exercises,
            rest_time=workout_out.rest_time,
            stress_questionnaire_time=workout_out.stress_questionnaire_time,
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


@router(
    response_model=list[
        schemas.TrainerSportsmanWorkoutOut
        | schemas.TrainerGroupWorkoutOut
        | schemas.TrainerTeamWorkoutOut
    ],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_workouts_for_sportsman(
    sportsman_email_in: EmailStr,
    self_trainer: Trainers = Depends(deps.self_trainer),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
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
    sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email_in)
    if not sportsman_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="_team must exist"
        )

    if sportsman_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

    s_workouts_out = await sportsmans_workouts_service.get_all_by_sportsman_id(
        sportsman_id=sportsman_out.id
    )
    workouts: list[
        schemas.TrainerSportsmanWorkoutOut
        | schemas.TrainerGroupWorkoutOut
        | schemas.TrainerTeamWorkoutOut
    ] = []
    for s_workout_out in s_workouts_out:
        workout_out = await workouts_service.get_by_id(id=s_workout_out.workout_id)
        if not workout_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_s_workout not in workout db",
            )

        trainer_workout_out = await trainers_workouts_service.get_by(
            workout_id=workout_out.id,
            trainer_id=self_trainer.id,
        )
        if not trainer_workout_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_s_workout not in trainer_workouts db",
            )

        base_workouts_schemas = schemas.TrainerWorkoutOut(
            id=workout_out.id,
            name=workout_out.workout_pool.name,
            estimated_time=workout_out.workout_pool.estimated_time,
            status=schemas.WorkoutsStatusesOut(
                status=consts.WorkoutsStatusesEnum(trainer_workout_out.status.status),
                description=consts.WORKOUTS_STATUSES_DESC[
                    consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
                ],
            ),
            date=workout_out.date,
            created_at=workout_out.workout_pool.created_at,
            exercises=workout_out.workout_pool.exercises,
            rest_time=workout_out.rest_time,
            stress_questionnaire_time=workout_out.stress_questionnaire_time,
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


@router(
    response_model=list[schemas.TrainerGroupWorkoutOut],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_workouts_for_group(
    id: UUID,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
) -> Any:
    group_id = id
    group_out = await groups_service.get_by_id(id=group_id)

    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group")

    g_workouts_out = await tgs_workouts_service.get_all_by_group_id(
        group_id=group_id,
    )
    workouts: list[schemas.TrainerGroupWorkoutOut] = []
    for g_workout_out in g_workouts_out:
        workout_out = await workouts_service.get_by_id(id=g_workout_out.workout_id)
        if not workout_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_g_workout not in workout db",
            )

        trainer_workout_out = await trainers_workouts_service.get_by(
            workout_id=workout_out.id,
            trainer_id=self_trainer.id,
        )
        if not trainer_workout_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_g_workout not in trainer_workouts db",
            )

        workout_schema = schemas.TrainerGroupWorkoutOut(
            id=workout_out.id,
            name=workout_out.workout_pool.name,
            estimated_time=workout_out.workout_pool.estimated_time,
            status=schemas.WorkoutsStatusesOut(
                status=consts.WorkoutsStatusesEnum(trainer_workout_out.status.status),
                description=consts.WORKOUTS_STATUSES_DESC[
                    consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
                ],
            ),
            date=workout_out.date,
            created_at=workout_out.workout_pool.created_at,
            exercises=workout_out.workout_pool.exercises,
            group_id=group_id,
            rest_time=workout_out.rest_time,
            stress_questionnaire_time=workout_out.stress_questionnaire_time,
        )
        workouts.append(workout_schema)

    return workouts


@router(
    response_model=list[schemas.TrainerTeamWorkoutOut],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_workouts_for_team(
    self_trainer: Trainers = Depends(deps.self_trainer),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="_team must exist"
        )

    t_workouts_out = await tgs_workouts_service.get_all_by_team_id(
        team_id=team_out.id,
    )
    workouts: list[schemas.TrainerTeamWorkoutOut] = []
    for t_workout_out in t_workouts_out:
        workout_out = await workouts_service.get_by_id(id=t_workout_out.workout_id)
        if not workout_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_s_workout not in workout db",
            )

        trainer_workout_out = await trainers_workouts_service.get_by(
            workout_id=workout_out.id,
            trainer_id=self_trainer.id,
        )
        if not trainer_workout_out:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="_t_workout not in trainer_workouts db",
            )

        workout_schema = schemas.TrainerTeamWorkoutOut(
            id=workout_out.id,
            name=workout_out.workout_pool.name,
            estimated_time=workout_out.workout_pool.estimated_time,
            status=schemas.WorkoutsStatusesOut(
                status=consts.WorkoutsStatusesEnum(trainer_workout_out.status.status),
                description=consts.WORKOUTS_STATUSES_DESC[
                    consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
                ],
            ),
            date=workout_out.date,
            created_at=workout_out.workout_pool.created_at,
            exercises=workout_out.workout_pool.exercises,
            team_id=team_out.id,
            rest_time=workout_out.rest_time,
            stress_questionnaire_time=workout_out.stress_questionnaire_time,
        )
        workouts.append(workout_schema)

    return workouts


@router(
    status_code=status.HTTP_204_NO_CONTENT,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def delete_workout(
    id: UUID,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
) -> None:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out or workout_out.workout_pool.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    time_now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    if time_now > workout_out.date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="workout")

    await workouts_service.delete(id=id)


@router(
    response_model=schemas.TrainerSportsmanWorkoutOut
    | schemas.TrainerGroupWorkoutOut
    | schemas.TrainerTeamWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def update_workout(
    id: UUID,
    update_workout_in: schemas.UpdateWorkoutIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> Any:
    old_workout_out = await workouts_service.get_by_id(id=id)
    if (
        not old_workout_out
        or old_workout_out.workout_pool.trainer_id != self_trainer.id
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    workout_out = await workouts_service.update(id=id, schema_in=update_workout_in)

    trainer_workout_out = await trainers_workouts_service.get_by(
        workout_id=workout_out.id,
        trainer_id=self_trainer.id,
    )
    if not trainer_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    base_workouts_schemas = schemas.TrainerWorkoutOut(
        id=workout_out.id,
        name=workout_out.workout_pool.name,
        estimated_time=workout_out.workout_pool.estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=consts.WorkoutsStatusesEnum(trainer_workout_out.status.status),
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
            ],
        ),
        date=workout_out.date,
        created_at=workout_out.workout_pool.created_at,
        exercises=workout_out.workout_pool.exercises,
        rest_time=workout_out.rest_time,
        stress_questionnaire_time=workout_out.stress_questionnaire_time,
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
