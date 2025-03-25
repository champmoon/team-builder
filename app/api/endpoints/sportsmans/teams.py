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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="team")

    team_out = await teams_service.get_by_id(id=self_sportsman.team_id)
    if team_out:
        return team_out
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="_team must exist",
    )


@router(
    response_model=schemas.SportsmanOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def join_team(
    confirm_token_in: schemas.ConfirmTokenIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
    tgs_workouts: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service],
    ),
) -> Any:
    if self_sportsman.team_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    invite_data = await auth_service.get_invite_data_by_confirm_token(
        confirm_token=str(confirm_token_in.confirm_token)
    )
    if not invite_data:
        raise HTTPException(status_code=status.HTTP_410_GONE)

    team_out = await teams_service.get_by_id(id=invite_data.team_id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    await sportsmans_service.add_to_team(
        sportsman_id=self_sportsman.id,
        team_id=team_out.id,
    )

    future_team_workouts_ids = await tgs_workouts_service.get_future_team_workouts_ids(
        team_id=team_out.id
    )
    await sportsmans_workouts_service.unbind_sportsman_to_workouts(
        sportsman_id=self_sportsman.id,
        workouts_ids=future_team_workouts_ids,
    )

    local_sportsman_id = invite_data.fake_id
    if not local_sportsman_id:
        return await sportsmans_service.get_by_id(id=self_sportsman.id)

    await sportsmans_groups_service.merge(
        local_sportsman_id=local_sportsman_id,
        true_sportsman_id=self_sportsman.id,
    )
    await sportsmans_workouts_service.merge(
        local_sportsman_id=local_sportsman_id,
        true_sportsman_id=self_sportsman.id,
    )
    await tgs_workouts.merge(
        local_sportsman_id=local_sportsman_id,
        true_sportsman_id=self_sportsman.id,
    )
    await sportsmans_service.delete(id=local_sportsman_id)

    return await sportsmans_service.get_by_id(id=self_sportsman.id)


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
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
) -> Any:
    if not self_sportsman.team_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="team")

    team_out = await teams_service.get_by_id(id=self_sportsman.team_id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
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
        future_group_workouts_ids = (
            await tgs_workouts_service.get_future_group_workouts_ids(
                group_id=sportsman_group.group_id
            )
        )
        await sportsmans_workouts_service.unbind_sportsman_to_workouts(
            sportsman_id=self_sportsman.id,
            workouts_ids=future_group_workouts_ids,
        )

    future_team_workouts_ids = await tgs_workouts_service.get_future_team_workouts_ids(
        team_id=team_out.id
    )
    await sportsmans_workouts_service.unbind_sportsman_to_workouts(
        sportsman_id=self_sportsman.id,
        workouts_ids=future_team_workouts_ids,
    )

    return await sportsmans_service.get_by_id(id=self_sportsman.id)
