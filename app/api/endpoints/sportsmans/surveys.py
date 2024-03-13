from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models.sportsmans import Sportsmans
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    status_code=status.HTTP_200_OK,
    response_model=schemas.SportsmanSurveysOut,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def get_survey(
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    sportsman_surveys_service: Services.sportsman_surveys = Depends(
        Provide[Containers.sportsman_surveys.service]
    ),
) -> Any:
    sportsman_surveys_out = await sportsman_surveys_service.get_by_sportsman_id(
        sportsman_id=self_sportsman.id
    )
    if sportsman_surveys_out:
        return sportsman_surveys_out
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="sportsman survey must exist",
    )


@router(
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def get_survey_update_flag(
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    sportsman_surveys_service: Services.sportsman_surveys = Depends(
        Provide[Containers.sportsman_surveys.service]
    ),
) -> Any:
    sportsman_surveys_out = await sportsman_surveys_service.get_by_sportsman_id(
        sportsman_id=self_sportsman.id
    )
    if not sportsman_surveys_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="sportsman survey must exist",
        )
    return (
        Response(status_code=status.HTTP_200_OK)
        if sportsman_surveys_out.update_it
        else Response(status_code=status.HTTP_423_LOCKED)
    )


@router(
    status_code=status.HTTP_200_OK,
    response_model=schemas.SportsmanSurveysOut,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def fill_survey(
    answers: list[schemas.SportsmanAnswerOut],
    self_sportsman: Sportsmans = Depends(deps.self_sportsman),
    sportsman_surveys_service: Services.sportsman_surveys = Depends(
        Provide[Containers.sportsman_surveys.service]
    ),
) -> Any:
    sportsman_surveys_out = await sportsman_surveys_service.get_by_sportsman_id(
        sportsman_id=self_sportsman.id
    )
    if not sportsman_surveys_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="sportsman survey must exist",
        )

    if sportsman_surveys_out.update_it is False:
        raise HTTPException(status_code=status.HTTP_423_LOCKED)

    return await sportsman_surveys_service.update(
        id=sportsman_surveys_out.id,
        answers=jsonable_encoder(answers),
    )
