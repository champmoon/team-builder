from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status, Response
from pydantic import TypeAdapter
from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Trainers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_workout_for_sportsman(
    create_workout_in: schemas.CreateWorkoutForSportsmanIn,
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    self_trainer: Trainers = Depends(deps.self_trainer),
) -> Any:
    sportsman_out = await sportsmans_service.get_by_id(
        id=create_workout_in.sportsman_id
    )
    if not sportsman_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sportsman not found"
        )
    
    return await workouts_service.create(
        trainer_id=self_trainer.id,
        schema_in=create_workout_in,
    )
