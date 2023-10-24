from typing import Any

from dependency_injector.wiring import inject
from fastapi import Depends, status

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.models import Trainers
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.TrainerOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_training(
    create_training_in,
    self_trainer: Trainers = Depends(deps.self_trainer),
) -> Any:
    return self_trainer
