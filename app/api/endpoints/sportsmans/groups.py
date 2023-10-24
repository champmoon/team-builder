from typing import Any
from uuid import UUID

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
    response_model=list[schemas.GroupOut],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
async def get_self_groups(
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
) -> Any:
    return self_sportsman.groups


@router(
    response_model=schemas.GroupOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def get_self_group(
    id: UUID,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
) -> Any:
    group_out = await groups_service.get_by_sportsman_id(
        id=id, sportsman_id=self_sportsman.id
    )
    if group_out:
        return group_out
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Group with id {id} not found",
    )


@router(
    response_model=schemas.SportsmanWithGroupsOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def outs_off_groups(
    groups_ids_in: schemas.ListGroupsIDsIn,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
) -> Any:
    for group_id in groups_ids_in.groups_ids:
        group_out = await groups_service.get_by_sportsman_id(
            id=group_id, sportsman_id=self_sportsman.id
        )
        if not group_out:
            continue

        await sportsmans_groups_service.delete(
            schema_in=schemas.DeleteSportsmanGroupIn(
                sportsman_id=self_sportsman.id,
                group_id=group_out.id,
            )
        )
    return await sportsmans_service.get_by_id(id=self_sportsman.id)


@router(
    response_model=schemas.SportsmanWithGroupsOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def out_off_group(
    id: UUID,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
) -> Any:
    group_out = await groups_service.get_by_sportsman_id(
        id=id, sportsman_id=self_sportsman.id
    )
    if not group_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {id} not found",
        )

    await sportsmans_groups_service.delete(
        schema_in=schemas.DeleteSportsmanGroupIn(
            sportsman_id=self_sportsman.id,
            group_id=group_out.id,
        )
    )
    return await sportsmans_service.get_by_id(id=self_sportsman.id)
