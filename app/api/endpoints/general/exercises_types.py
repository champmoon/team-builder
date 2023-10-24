from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app import consts, schemas
from app.api import deps
from app.containers import Containers
from app.services import Services
from app.utils import UsersScope
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=list[schemas.ExercisesTypesOut],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=UsersScope.all())
@inject
async def get_exercises_types(
    exercises_types_service: Services.exercises_types = Depends(
        Provide[Containers.exercises_types.service],
    )
) -> Any:
    exercises_types_out = await exercises_types_service.get_all()
    print(len(consts.ExercisesTypesEnum))
    return exercises_types_out
