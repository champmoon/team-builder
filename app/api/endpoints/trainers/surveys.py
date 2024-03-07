from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.api import deps
from app.cache.actions import ConfirmTrainerEmailAction
from app.conf.settings import settings
from app.consts import UsersTypes
from app.containers import Containers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()

@router(
    status_code=status.HTTP_200_OK,
)
# @deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_survey(
    team_surveys_service: Services.team_surveys = Depends(
        Provide[Containers.team_surveys.service],
    ),
) -> Any:
    return await team_surveys_service.get_all()
