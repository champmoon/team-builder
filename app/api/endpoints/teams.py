from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.api import deps
from app.containers import Containers
from app.services import Services
from app.utils import UsersScope
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.TeamOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=UsersScope.all())
@inject
async def get_team_by_trainer_id(
    trainer_id: UUID,
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    trainers_service: Services.trainers = Depends(
        Provide[Containers.trainers.service],
    ),
) -> Any:
    trainer_out = await trainers_service.get_by_id(id=trainer_id)
    if not trainer_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trainer with id - {trainer_out} not found",
        )

    team_out = await teams_service.get_by_trainer_id(trainer_id=trainer_id)
    if team_out:
        return team_out
    return await teams_service.create(
        schema_in=schemas.CreateTeamIn(trainer_id=trainer_id)
    )


@router(
    response_model=schemas.TeamOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=UsersScope.all())
@inject
async def get_team_by_id(
    id: UUID,
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_id(id=id)
    if team_out:
        return team_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Team with id - {id} not found",
    )
