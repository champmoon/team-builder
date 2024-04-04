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
    response_model=list[schemas.StressQuestionnaireOut],
    status_code=status.HTTP_200_OK,
)
@inject
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
async def get_active_stress_questionnaires(
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
) -> Any:
    return await stress_questionnaires_service.get_active_stress_questionnaires(
        sportsman_id=self_sportsman.id
    )
