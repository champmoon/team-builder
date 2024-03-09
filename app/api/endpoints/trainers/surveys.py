from typing import Any, cast

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.api import deps
from app.cache.actions import ConfirmTrainerEmailAction
from app.conf.settings import settings
from app.consts import UsersTypes
from app.containers import Containers
from app.models.trainers import Trainers
from app.services import Services
from app.utils.router import EndPointRouter
from fastapi.encoders import jsonable_encoder

router = EndPointRouter()


@router(
    status_code=status.HTTP_200_OK,
    response_model=schemas.TeamSurveysOut,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_survey(
    self_trainer: Trainers = Depends(deps.self_trainer),
    team_surveys_service: Services.team_surveys = Depends(
        Provide[Containers.team_surveys.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Team must exist",
        )

    team_survey_out = await team_surveys_service.get_by_team_id(team_id=team_out.id)
    if not team_survey_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="team survey must exist",
        )

    return team_survey_out


@router(
    status_code=status.HTTP_200_OK,
    response_model=schemas.TeamSurveysOut,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def update_survey(
    add_fields_in: schemas.TeamSurveysAddFieldsUpdateIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    team_surveys_service: Services.team_surveys = Depends(
        Provide[Containers.team_surveys.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Team must exist",
        )

    team_survey_out = await team_surveys_service.get_by_team_id(team_id=team_out.id)
    if not team_survey_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="team survey must exist",
        )

    return await team_surveys_service.update(
        id=team_survey_out.id, add_fields=jsonable_encoder(add_fields_in.add_fields)
    )
