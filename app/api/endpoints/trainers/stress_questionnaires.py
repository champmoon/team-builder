from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
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
    response_model=list[schemas.StressQuestionnaireOut],
    status_code=status.HTTP_200_OK,
)
@inject
@deps.auth_required(users=[UsersTypes.TRAINER])
async def get_all_stress_questionnaires_by_sportsman(
    email: EmailStr,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    sportsman_out = await sportsmans_service.get_by_email(email=email)
    if not sportsman_out or sportsman_out.team_id != team_out.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

    return await stress_questionnaires_service.get_all_by_sportsman_id(
        sportsman_id=sportsman_out.id
    )


@router(
    response_model=list[schemas.StressQuestionnaireOut],
    status_code=status.HTTP_200_OK,
)
@inject
@deps.auth_required(users=[UsersTypes.TRAINER])
async def get_all_stress_questionnaires_by_workout(
    id: UUID,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out or workout_out.workout_pool.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    return await stress_questionnaires_service.get_all_by_workout_id(workout_id=id)


@router(
    response_model=schemas.StressQuestionnaireOut,
    status_code=status.HTTP_200_OK,
)
@inject
@deps.auth_required(users=[UsersTypes.TRAINER])
async def get_stress_questionnaire(
    id: UUID,
    _: Trainers = Depends(deps.self_trainer),
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
