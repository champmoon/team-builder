from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Sportsmans
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.TeamOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def get_self_team(
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    if not self_sportsman.team_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    team_out = await teams_service.get_by_id(id=self_sportsman.team_id)
    if team_out:
        return team_out
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Team must exist",
    )


@router(
    response_model=schemas.SportsmanOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def out_off_team(
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
) -> Any:
    if not self_sportsman.team_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )

    team_out = await teams_service.get_by_id(id=self_sportsman.team_id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Team must exist",
        )

    await sportsmans_service.kick_off_team(sportsman_id=self_sportsman.id)

    sportsmans_groups = await sportsmans_groups_service.get_all_groups_by_sportsman_id(
        sportsman_id=self_sportsman.id
    )
    for sportsman_group in sportsmans_groups:
        await sportsmans_groups_service.delete(
            schema_in=schemas.DeleteSportsmanGroupIn(
                sportsman_id=self_sportsman.id,
                group_id=sportsman_group.group_id,
            )
        )

    return await sportsmans_service.get_by_id(id=self_sportsman.id)
