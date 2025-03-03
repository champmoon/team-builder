from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from pydantic import EmailStr

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models.trainers import Trainers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    status_code=status.HTTP_200_OK,
    response_model=schemas.TeamSurveysOut,
    deprecated=True
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
            detail="_team must exist",
        )

    team_survey_out = await team_surveys_service.get_by_team_id(team_id=team_out.id)
    if not team_survey_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team survey must exist",
        )

    return team_survey_out


@router(
    status_code=status.HTTP_200_OK,
    response_model=schemas.TeamSurveysOut,
    deprecated=True
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
            detail="_team must exist",
        )

    team_survey_out = await team_surveys_service.get_by_team_id(team_id=team_out.id)
    if not team_survey_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team survey must exist",
        )

    return await team_surveys_service.update(
        id=team_survey_out.id, add_fields=jsonable_encoder(add_fields_in.add_fields)
    )


@router(
    status_code=status.HTTP_200_OK,
    deprecated=True
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def set_update_sportsman_survey(
    email: EmailStr,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    sportsman_surveys_service: Services.sportsman_surveys = Depends(
        Provide[Containers.sportsman_surveys.service]
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    sportsman_out = await sportsmans_service.get_by_email(email=email)
    if not sportsman_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

    if sportsman_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

    await sportsman_surveys_service.set_update(sportsman_id=sportsman_out.id)

    return Response(status_code=status.HTTP_200_OK)


@router(
    status_code=status.HTTP_200_OK,
    deprecated=True
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def set_update_team_survey(
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    sportsman_surveys_service: Services.sportsman_surveys = Depends(
        Provide[Containers.sportsman_surveys.service]
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    sportsmans_out = await sportsmans_service.get_by_team_id(team_id=team_out.id)
    for sportsman_out in sportsmans_out:
        await sportsman_surveys_service.set_update(sportsman_id=sportsman_out.id)

    return Response(status_code=status.HTTP_200_OK)


@router(
    status_code=status.HTTP_200_OK,
    response_model=schemas.SportsmanSurveysOut,
    deprecated=True
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_sportsman_survey(
    email: EmailStr,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    sportsman_surveys_service: Services.sportsman_surveys = Depends(
        Provide[Containers.sportsman_surveys.service]
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    sportsman_out = await sportsmans_service.get_by_email(email=email)
    if not sportsman_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

    if sportsman_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

    sportsman_surveys_out = await sportsman_surveys_service.get_by_sportsman_id(
        sportsman_id=sportsman_out.id
    )
    if sportsman_surveys_out:
        return sportsman_surveys_out
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="_sportsman survey must exist",
    )


@router(
    status_code=status.HTTP_200_OK,
    response_model=schemas.SportsmanSurveysOut,
    deprecated=True
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def fill_survey_for_sportsman(
    email: EmailStr,
    answers: list[schemas.SportsmanAnswerOut],
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    sportsman_surveys_service: Services.sportsman_surveys = Depends(
        Provide[Containers.sportsman_surveys.service]
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    sportsman_out = await sportsmans_service.get_by_email(email=email)
    if not sportsman_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

    if sportsman_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

    sportsman_surveys_out = await sportsman_surveys_service.get_by_sportsman_id(
        sportsman_id=sportsman_out.id
    )
    if not sportsman_surveys_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_sportsman survey must exist",
        )

    return await sportsman_surveys_service.update(
        id=sportsman_surveys_out.id,
        answers=jsonable_encoder(answers),
    )
