from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import consts, schemas
from app.api import deps
from app.containers import Containers
from app.models import Sportsmans
from app.services import Services
from app.utils import UsersScope
from app.utils.router import EndPointRouter

router = EndPointRouter()


@inject
async def get_self_trainer_id(
    sportsman_out: Sportsmans,
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> UUID:
    if not sportsman_out.team_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="sportsman_team"
        )

    team_out = await teams_service.get_by_id(id=sportsman_out.team_id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="sportsman_team"
        )
    return team_out.trainer_id


@router(
    response_model=list[schemas.ExercisesTypesOut],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=UsersScope.all())
@inject
async def get_exercises_types(
    token: schemas.TokensDecodedSchema = Depends(deps.get_authorization_data),
    exercises_types_service: Services.exercises_types = Depends(
        Provide[Containers.exercises_types.service]
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service]
    ),
    trainers_service: Services.trainers = Depends(
        Provide[Containers.trainers.service],
    ),
) -> Any:
    user_id = UUID(token.user_id)
    if token.user_type == consts.UsersTypes.SPORTSMAN:
        sportsman_out = await sportsmans_service.get_by_id(id=user_id)
        if not sportsman_out:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return await exercises_types_service.get_all(
            trainer_id=await get_self_trainer_id(sportsman_out=sportsman_out)
        )

    if token.user_type == consts.UsersTypes.TRAINER:
        trainer_out = await trainers_service.get_by_id(id=user_id)
        if not trainer_out:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        return await exercises_types_service.get_all(trainer_id=trainer_out.id)

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
