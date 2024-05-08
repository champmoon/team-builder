from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, status

from app import schemas
from app.api import deps
from app.consts import WORKOUTS_STATUSES_DESC, WorkoutsStatusesEnum
from app.containers import Containers
from app.services import Services
from app.utils import UsersScope
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=list[schemas.WorkoutsStatusesOut],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=UsersScope.all())
@inject
async def get_workouts_statuses(
    workouts_statuses_service: Services.workouts_statuses = Depends(
        Provide[Containers.workouts_statuses.service],
    )
) -> Any:
    response: list[schemas.WorkoutsStatusesOut] = []
    workouts_statuses_out = await workouts_statuses_service.get_all()
    for workout_status_out in workouts_statuses_out:
        response.append(
            schemas.WorkoutsStatusesOut(
                status=WorkoutsStatusesEnum(workout_status_out.status),
                description=WORKOUTS_STATUSES_DESC[
                    WorkoutsStatusesEnum(workout_status_out.status)
                ],
            )
        )
    return response
