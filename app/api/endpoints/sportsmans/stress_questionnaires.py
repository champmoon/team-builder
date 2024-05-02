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
    return await stress_questionnaires_service.get_actives(
        sportsman_id=self_sportsman.id
    )


@router(
    response_model=list[schemas.StressQuestionnaireOut],
    status_code=status.HTTP_200_OK,
)
@inject
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
async def get_all_stress_questionnaires(
    start_date: NaiveDatetime | None = None,
    end_date: NaiveDatetime | None = None,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
) -> Any:
    return await stress_questionnaires_service.get_past_by_sportsman_id(
        sportsman_id=self_sportsman.id,
        start_date=start_date,
        end_date=end_date,
    )


@router(
    response_model=schemas.StressQuestionnaireOut,
    status_code=status.HTTP_200_OK,
)
@inject
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
async def get_stress_questionnaire(
    id: UUID,
    _: Sportsmans = Depends(deps.self_sportsman),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
) -> Any:
    stress_questionnaires_out = await stress_questionnaires_service.get_by_id(id=id)
    if not stress_questionnaires_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="stress_questionnaire"
        )
    return stress_questionnaires_out


@router(
    response_model=schemas.StressQuestionnaireOut,
    status_code=status.HTTP_200_OK,
)
@inject
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
async def get_stress_questionnaire_by_workout_id(
    workout_id: UUID,
    _: Sportsmans = Depends(deps.self_sportsman),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
) -> Any:
    stress_questionnaires_out = await stress_questionnaires_service.get_by_workout_id(
        workout_id=workout_id
    )
    if not stress_questionnaires_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="stress_questionnaire"
        )
    return stress_questionnaires_out


@router(
    response_model=schemas.StressQuestionnaireOut,
    status_code=status.HTTP_200_OK,
)
@inject
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
async def fill_stress_questionnaire(
    id: UUID,
    update_stress_questionnaire_in: schemas.UpdateStressQuestionnaireIn,
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
) -> Any:
    updated_stress_questionnaire_out = await stress_questionnaires_service.update(
        id=id,
        sportsman_id=self_sportsman.id,
        schema_in=update_stress_questionnaire_in,
    )
    if not updated_stress_questionnaire_out:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="stress_questionnaire"
        )

    return updated_stress_questionnaire_out
