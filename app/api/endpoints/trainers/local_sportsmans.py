from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Trainers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=list[schemas.SportsmanOut] | schemas.SportsmanOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_local_sportsmans(
    id: UUID | None = None,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not id:
        all_sportsmans_out = await sportsmans_service.get_by_team_id(
            team_id=team_out.id
        )
        fakes_out = [
            fake_out for fake_out in all_sportsmans_out if fake_out.email is None
        ]
        return fakes_out

    fake_out = await sportsmans_service.get_by_id(id=id)
    if not fake_out or fake_out.email is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if fake_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return fake_out


@router(
    response_model=schemas.SportsmanOut,
    status_code=status.HTTP_201_CREATED,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_local_sportsmans(
    create_sportsman_in: schemas.CreateLocalSportsmanIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    new_fake_out = await sportsmans_service.create_local(
        team_id=team_out.id, schema_in=create_sportsman_in
    )

    return new_fake_out


@router(
    response_model=schemas.SportsmanOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def update_local_sportsman(
    id: UUID,
    update_sportsman_in: schemas.UpdateSportsmanIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    fake_out = await sportsmans_service.get_by_id(id=id)
    if not fake_out or fake_out.email is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if fake_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return await sportsmans_service.update(
        id=id,
        schema_in=update_sportsman_in,
    )


@router(
    response_model=schemas.SportsmanOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def delete_local_sportsmans(
    id: UUID,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    fake_out = await sportsmans_service.get_by_id(id=id)
    if not fake_out or fake_out.email is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if fake_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await sportsmans_service.delete(id=id)
    return fake_out


@router(
    response_model=schemas.SportsmanOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def merge_local_sportsman(
    merge_sportsman_in: schemas.MergeLocalSportsman,
    self_trainer: Trainers = Depends(deps.self_trainer),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service],
    ),
    tgs_workouts: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    fake_out = await sportsmans_service.get_by_id(
        id=merge_sportsman_in.local_sportsman_id
    )
    if not fake_out or fake_out.email is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if fake_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try_out = await sportsmans_service.get_by_email(email=merge_sportsman_in.email)
    if not try_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if try_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await sportsmans_groups_service.merge(
        local_sportsman_id=fake_out.id,
        true_sportsman_id=try_out.id,
    )
    await sportsmans_workouts_service.merge(
        local_sportsman_id=fake_out.id,
        true_sportsman_id=try_out.id,
    )
    await tgs_workouts.merge(
        local_sportsman_id=fake_out.id,
        true_sportsman_id=try_out.id,
    )
    await sportsmans_service.delete(id=fake_out.id)
    return try_out
