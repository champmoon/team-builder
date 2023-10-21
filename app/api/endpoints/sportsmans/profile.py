from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Sportsmans
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.SportsmanOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def get_profile(
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
) -> Any:
    return self_sportsman


@router(
    response_model=schemas.SportsmanOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def update_profile(
    update_sportsman_in: schemas.UpdateSportsmanIn,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
) -> Any:
    return await sportsmans_service.update(
        id=self_sportsman.id,
        schema_in=update_sportsman_in,
    )
