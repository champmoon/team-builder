from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Trainers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.TrainerOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_profile(
    self_trainer: Trainers = Depends(deps.self_trainer),
) -> Any:
    return self_trainer


@router(
    response_model=schemas.TrainerOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def update_profile(
    update_trainer_in: schemas.UpdateTrainerIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    trainers_service: Services.trainers = Depends(
        Provide[Containers.trainers.service],
    ),
) -> Any:
    return await trainers_service.update(
        id=self_trainer.id,
        schema_in=update_trainer_in,
    )
