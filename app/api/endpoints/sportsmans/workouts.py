from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from pydantic import NaiveDatetime

from app import consts, schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Sportsmans
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=list[
        schemas.SportsmansSportsmanWorkoutOut
        | schemas.SportsmansGroupWorkoutOut
        | schemas.SportsmansTeamWorkoutOut
    ],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def get_workouts(
    offset: int = 0,
    limit: int = 100,
    start_date: NaiveDatetime | None = None,
    end_date: NaiveDatetime | None = None,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> Any:
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
            status=schemas.WorkoutsStatusesOut(
                status=consts.WorkoutsStatusesEnum(
                    sportsmans_workout_out.status.status
                ),
                description=consts.WORKOUTS_STATUSES_DESC[
                    consts.WorkoutsStatusesEnum(sportsmans_workout_out.status.status)
                ],
            ),
            date=workout_out.date,
            created_at=workout_out.workout_pool.created_at,
            exercises=workout_out.workout_pool.exercises,
            rest_time=workout_out.rest_time,
            stress_questionnaire_time=workout_out.stress_questionnaire_time,
            comment=workout_out.comment,
            goal=workout_out.goal,
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
    response_model=(
        schemas.SportsmansSportsmanWorkoutOut
        | schemas.SportsmansGroupWorkoutOut
        | schemas.SportsmansTeamWorkoutOut
    ),
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def get_workout(
    id: UUID,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    sportsman_workout_out = await sportsmans_workouts_service.get_by(
        workout_id=workout_out.id, sportsman_id=self_sportsman.id
    )
    if not sportsman_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    base_workouts_schemas = schemas.TrainerWorkoutOut(
        id=workout_out.id,
        name=workout_out.workout_pool.name,
        estimated_time=workout_out.workout_pool.estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status),
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            ],
        ),
        date=workout_out.date,
        created_at=workout_out.workout_pool.created_at,
        exercises=workout_out.workout_pool.exercises,
        rest_time=workout_out.rest_time,
        stress_questionnaire_time=workout_out.stress_questionnaire_time,
        comment=workout_out.comment,
        goal=workout_out.goal,
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
            sportsman_id=sportsman_id,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_tgs all none ids",
        )

    return workout_schema


@router(
    response_model=(
        schemas.SportsmansSportsmanWorkoutOut
        | schemas.SportsmansGroupWorkoutOut
        | schemas.SportsmansTeamWorkoutOut
    ),
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def start_workout(
    id: UUID,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    sportsman_workout_out = await sportsmans_workouts_service.get_by(
        workout_id=workout_out.id, sportsman_id=self_sportsman.id
    )
    if not sportsman_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    sportsman_workout_out = await sportsmans_workouts_service.in_progress(
        schema_in=schemas.UpdateSportsmansWorkoutIn(
            sportsman_id=self_sportsman.id,
            workout_id=workout_out.id,
        )
    )

    base_workouts_schemas = schemas.TrainerWorkoutOut(
        id=workout_out.id,
        name=workout_out.workout_pool.name,
        estimated_time=workout_out.workout_pool.estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status),
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            ],
        ),
        date=workout_out.date,
        created_at=workout_out.workout_pool.created_at,
        exercises=workout_out.workout_pool.exercises,
        rest_time=workout_out.rest_time,
        stress_questionnaire_time=workout_out.stress_questionnaire_time,
        comment=workout_out.comment,
        goal=workout_out.goal,
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
            sportsman_id=sportsman_id,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_tgs all none ids",
        )

    return workout_schema


@router(
    response_model=(
        schemas.SportsmansSportsmanWorkoutOut
        | schemas.SportsmansGroupWorkoutOut
        | schemas.SportsmansTeamWorkoutOut
    ),
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def complete_workout(
    id: UUID,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
    health_questionnaires_service: Services.health_questionnaires = Depends(
        Provide[Containers.health_questionnaires.service],
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    sportsman_workout_out = await sportsmans_workouts_service.get_by(
        workout_id=workout_out.id, sportsman_id=self_sportsman.id
    )
    if not sportsman_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    sportsman_workout_out = await sportsmans_workouts_service.completed(
        schema_in=schemas.UpdateSportsmansWorkoutIn(
            sportsman_id=self_sportsman.id,
            workout_id=workout_out.id,
        )
    )

    base_workouts_schemas = schemas.TrainerWorkoutOut(
        id=workout_out.id,
        name=workout_out.workout_pool.name,
        estimated_time=workout_out.workout_pool.estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status),
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            ],
        ),
        date=workout_out.date,
        created_at=workout_out.workout_pool.created_at,
        exercises=workout_out.workout_pool.exercises,
        rest_time=workout_out.rest_time,
        stress_questionnaire_time=workout_out.stress_questionnaire_time,
        comment=workout_out.comment,
        goal=workout_out.goal,
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
            sportsman_id=sportsman_id,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_tgs all none ids",
        )

    await stress_questionnaires_service.create(
        schema_in=schemas.CreateStressQuestionnaireIn(
            sportsman_id=self_sportsman.id,
            workout_id=workout_out.id,
        ),
        timeout=workout_out.stress_questionnaire_time,
    )
    await health_questionnaires_service.set_on_next_day(sportsman_id=self_sportsman.id)

    return workout_schema
