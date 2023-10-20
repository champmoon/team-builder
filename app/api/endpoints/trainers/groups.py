from typing import Any

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
    response_model=list[schemas.GroupOut],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_self_groups(
    self_trainer: Trainers = Depends(deps.self_trainer),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
) -> Any:
    return await groups_service.get_all_by_trainer_id(trainer_id=self_trainer.id)


@router(
    response_model=schemas.GroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_group(
    create_group_in: schemas.CreateGroupIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
) -> Any:
    new_group_out = await groups_service.create(
        schema_in=create_group_in,
        trainer_id=self_trainer.id,
    )
    if not create_group_in.sportsmans_emails:
        return new_group_out

    sportsmans_emails = create_group_in.sportsmans_emails
    for sportsman_email in sportsmans_emails:
        sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
        if not sportsman_out:
            continue

        await sportsmans_groups_service.create(
            schema_in=schemas.CreateSportsmanGroupIn(
                sportsman_id=sportsman_out.id,
                group_id=new_group_out.id,
            )
        )

    return await groups_service.get_by_id(id=new_group_out.id)


@router(
    response_model=schemas.GroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def adds_sportsman_to_group(
    add_sportsman_to_group_in: schemas.AddSportsmanToGroupIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
) -> Any:
    group_id = add_sportsman_to_group_in.group_id
    sportsman_email = add_sportsman_to_group_in.sportsman_email

    group_out = await groups_service.get_by_id(id=group_id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found",
        )

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Team must exist",
        )

    sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
    if not sportsman_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sportsman with email {sportsman_email} not found",
        )

    if sportsman_out.team_id != team_out.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Sportsman with email {sportsman_email} not be on a team",
        )

    await sportsmans_groups_service.create(
        schema_in=schemas.CreateSportsmanGroupIn(
            sportsman_id=sportsman_out.id,
            group_id=group_out.id,
        )
    )

    return await groups_service.get_by_id(id=group_out.id)


@router(
    response_model=schemas.GroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def adds_sportsmans_to_group(
    add_sportsman_to_group_in: schemas.AddSportsmansToGroupIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
) -> Any:
    group_id = add_sportsman_to_group_in.group_id
    sportsmans_emails = add_sportsman_to_group_in.sportsmans_emails

    group_out = await groups_service.get_by_id(id=group_id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found",
        )

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Team must exist",
        )

    for sportsman_email in sportsmans_emails:
        sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
        if not sportsman_out or sportsman_out.team_id != team_out.id:
            continue

        await sportsmans_groups_service.create(
            schema_in=schemas.CreateSportsmanGroupIn(
                sportsman_id=sportsman_out.id,
                group_id=group_out.id,
            )
        )

    return await groups_service.get_by_id(id=group_out.id)
