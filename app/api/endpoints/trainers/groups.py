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
    response_model=list[schemas.GroupOut] | schemas.GroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_self_groups(
    id: UUID | None = None,
    self_trainer: Trainers = Depends(deps.self_trainer),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
) -> Any:
    if not id:
        return await groups_service.get_all_by_trainer_id(trainer_id=self_trainer.id)
    group_out = await groups_service.get_by_id(id=id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group")
    return group_out


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
    response_model=schemas.OnlyGroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def update_group(
    id: UUID,
    update_group_in: schemas.UpdateGroupIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
) -> Any:
    group_out = await groups_service.get_by_id(id=id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group")
    return await groups_service.update(id=id, schema_in=update_group_in)


@router(
    response_model=schemas.GroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def delete_group(
    id: UUID,
    self_trainer: Trainers = Depends(deps.self_trainer),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> Any:
    group_out = await groups_service.get_by_id(id=id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group")

    future_group_workouts_ids = (
        await tgs_workouts_service.get_future_group_workouts_ids(group_id=group_out.id)
    )
    await workouts_service.delete_many(ids=future_group_workouts_ids)

    await groups_service.delete(id=id)
    return group_out


@router(
    response_model=schemas.GroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def add_sportsman_to_group(
    add_sportsman_to_group_in: schemas.SportsmanToGroupIn,
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
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
) -> Any:
    group_id = add_sportsman_to_group_in.group_id
    sportsman_email = add_sportsman_to_group_in.sportsman_email

    group_out = await groups_service.get_by_id(id=group_id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group")

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
    if not sportsman_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

    if sportsman_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

    sportsman_group_out = await sportsmans_groups_service.get_by(
        sportsman_id=sportsman_out.id, group_id=group_id
    )
    if sportsman_group_out:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

    await sportsmans_groups_service.create(
        schema_in=schemas.CreateSportsmanGroupIn(
            sportsman_id=sportsman_out.id,
            group_id=group_out.id,
        )
    )

    future_group_workouts_ids = (
        await tgs_workouts_service.get_future_group_workouts_ids(group_id=group_out.id)
    )
    await sportsmans_workouts_service.bind_sportsman_to_workouts(
        sportsman_id=sportsman_out.id,
        workouts_ids=future_group_workouts_ids,
    )

    return await groups_service.get_by_id(id=group_out.id)


@router(
    response_model=schemas.GroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def adds_sportsmans_to_group(
    adds_sportsmans_to_group_in: schemas.SportsmansToGroupIn,
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
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
) -> Any:
    group_id = adds_sportsmans_to_group_in.group_id
    sportsmans_emails = adds_sportsmans_to_group_in.sportsmans_emails

    group_out = await groups_service.get_by_id(id=group_id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group")

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    future_group_workouts_ids = (
        await tgs_workouts_service.get_future_group_workouts_ids(group_id=group_out.id)
    )
    for sportsman_email in sportsmans_emails or []:
        sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
        if not sportsman_out or sportsman_out.team_id != team_out.id:
            continue

        sportsman_group_out = await sportsmans_groups_service.get_by(
            sportsman_id=sportsman_out.id, group_id=group_id
        )
        if sportsman_group_out:
            continue

        await sportsmans_groups_service.create(
            schema_in=schemas.CreateSportsmanGroupIn(
                sportsman_id=sportsman_out.id,
                group_id=group_out.id,
            )
        )

        await sportsmans_workouts_service.bind_sportsman_to_workouts(
            sportsman_id=sportsman_out.id,
            workouts_ids=future_group_workouts_ids,
        )

    return await groups_service.get_by_id(id=group_out.id)


@router(
    response_model=schemas.GroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def kick_sportsman_off_group(
    kick_sportsman_to_group_in: schemas.SportsmanToGroupIn,
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
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
) -> Any:
    group_id = kick_sportsman_to_group_in.group_id
    sportsman_email = kick_sportsman_to_group_in.sportsman_email

    group_out = await groups_service.get_by_id(id=group_id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group")

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
    if not sportsman_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

    if sportsman_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

    await sportsmans_groups_service.delete(
        schema_in=schemas.DeleteSportsmanGroupIn(
            sportsman_id=sportsman_out.id,
            group_id=group_out.id,
        )
    )

    future_group_workouts_ids = (
        await tgs_workouts_service.get_future_group_workouts_ids(group_id=group_out.id)
    )
    await sportsmans_workouts_service.unbind_sportsman_to_workouts(
        sportsman_id=sportsman_out.id,
        workouts_ids=future_group_workouts_ids,
    )

    return await groups_service.get_by_id(id=group_out.id)


@router(
    response_model=schemas.GroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def kicks_sportsmans_off_group(
    kicks_sportsmans_to_group_in: schemas.SportsmansToGroupIn,
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
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
) -> Any:
    group_id = kicks_sportsmans_to_group_in.group_id
    sportsmans_emails = kicks_sportsmans_to_group_in.sportsmans_emails

    group_out = await groups_service.get_by_id(id=group_id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="group")

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    future_group_workouts_ids = (
        await tgs_workouts_service.get_future_group_workouts_ids(group_id=group_out.id)
    )
    for sportsman_email in sportsmans_emails or []:
        sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
        if not sportsman_out or sportsman_out.team_id != team_out.id:
            continue

        await sportsmans_groups_service.delete(
            schema_in=schemas.DeleteSportsmanGroupIn(
                sportsman_id=sportsman_out.id,
                group_id=group_out.id,
            )
        )

        await sportsmans_workouts_service.unbind_sportsman_to_workouts(
            sportsman_id=sportsman_out.id,
            workouts_ids=future_group_workouts_ids,
        )

    return await groups_service.get_by_id(id=group_out.id)
