from typing import Any
from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, UploadFile, status

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Sportsmans
from app.services import Services
from app.utils import SystemFile
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


@router(
    response_model=schemas.TrainerOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def upload_avatar(
    avatar: UploadFile,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
) -> Any:
    file_id = uuid4()

    system_file = SystemFile(
        bytes_buffer=avatar.file,
        dir_path=str(file_id),
        filename=avatar.filename,
    )
    new_avatar_uri = system_file.save()

    return await sportsmans_service.update_avatar(
        id=self_sportsman.id,
        avatar_uri=new_avatar_uri,
    )
