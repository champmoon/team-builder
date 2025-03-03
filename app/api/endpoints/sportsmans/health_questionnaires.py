from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from pydantic import NaiveDatetime

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Sportsmans
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.HealthQuestionnaireOut,
    status_code=status.HTTP_200_OK,
    deprecated=True,
)
@inject
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
async def get_active_health_questionnaire(
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    health_questionnaires_service: Services.health_questionnaires = Depends(
        Provide[Containers.health_questionnaires.service],
    ),
) -> Any:
    health_questionnaire_out = await health_questionnaires_service.get_active(
        sportsman_id=self_sportsman.id
    )
    if health_questionnaire_out:
        return health_questionnaire_out

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="health_questionnaire"
    )


@router(
    response_model=list[schemas.HealthQuestionnaireOut],
    status_code=status.HTTP_200_OK,
    deprecated=True,
)
@inject
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
async def get_all_health_questionnaires(
    start_date: NaiveDatetime | None = None,
    end_date: NaiveDatetime | None = None,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    health_questionnaires_service: Services.health_questionnaires = Depends(
        Provide[Containers.health_questionnaires.service],
    ),
) -> Any:
    return await health_questionnaires_service.get_by_sportsman_id(
        sportsman_id=self_sportsman.id,
        start_date=start_date,
        end_date=end_date,
    )


@router(
    response_model=schemas.HealthQuestionnaireOut,
    status_code=status.HTTP_200_OK,
    deprecated=True,
)
@inject
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
async def get_health_questionnaire(
    id: UUID,
    _: Sportsmans = Depends(deps.self_sportsman),
    health_questionnaires_service: Services.health_questionnaires = Depends(
        Provide[Containers.health_questionnaires.service],
    ),
) -> Any:
    health_questionnaires_out = await health_questionnaires_service.get_by_id(id=id)
    if health_questionnaires_out:
        return health_questionnaires_out

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="health_questionnaire"
    )


@router(
    response_model=schemas.HealthQuestionnaireOut,
    status_code=status.HTTP_200_OK,
    deprecated=True,
)
@inject
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
async def fill_health_questionnaire(
    id: UUID,
    update_health_questionnaire_in: schemas.UpdateHealthQuestionnaireIn,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    health_questionnaires_service: Services.health_questionnaires = Depends(
        Provide[Containers.health_questionnaires.service],
    ),
) -> Any:
    updated_health_questionnaire_out = await health_questionnaires_service.update(
        id=id,
        sportsman_id=self_sportsman.id,
        schema_in=update_health_questionnaire_in,
    )
    if not updated_health_questionnaire_out:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="health_questionnaire"
        )

    return updated_health_questionnaire_out
