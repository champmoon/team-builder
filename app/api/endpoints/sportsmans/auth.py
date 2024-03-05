from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.api import deps
from app.cache.actions import ConfirmSportsmanEmailAction
from app.conf.settings import settings
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Trainers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    status_code=status.HTTP_202_ACCEPTED,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def send_confirm_sportsman_email(
    sportsman_email_confirm_in: schemas.SendSportsmanEmailIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    sportsmans_service: Services.trainers = Depends(
        Provide[Containers.sportsmans.service]
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    self_trainer: Trainers = Depends(deps.self_trainer),
) -> Any:
    is_blocked = await auth_service.is_email_sended(sportsman_email_confirm_in.email)

    if is_blocked:
        timer = await auth_service.get_email_block_timer(
            email=sportsman_email_confirm_in.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "email already sended", "expire": timer},
        )

    sportsman_out = await sportsmans_service.get_by_email(
        email=sportsman_email_confirm_in.email
    )
    if sportsman_out:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Sportsman with email {sportsman_email_confirm_in.email} already"
                " exists"
            ),
        )

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Team must exist",
        )

    confirm_data = schemas.InnerSendSportsmanEmailIn(
        email=sportsman_email_confirm_in.email,
        sport_type=team_out.sport_type,
        trainer_id=self_trainer.id,
    )

    if settings.DEBUG:
        confirmation_uri = await auth_service.create_sportsman_confirmation_uri(
            confirm_data=confirm_data
        )
        await auth_service.set_email_sended(email=sportsman_email_confirm_in.email)

        return {"uri": confirmation_uri, "expire": ConfirmSportsmanEmailAction.timeout}

    await auth_service.send_sportsman_confirmation_email(confirm_data=confirm_data)
    await auth_service.set_email_sended(email=sportsman_email_confirm_in.email)

    return {"expire": ConfirmSportsmanEmailAction.timeout}


@router(
    response_model=schemas.SportsmanEmailConfirmOut,
    status_code=status.HTTP_200_OK,
)
@inject
async def confirm_sportsman_email(
    confirm_token_in: schemas.ConfirmTokenIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
) -> Any:
    sportsman_data_out = await auth_service.get_sportsman_data_by_confirm_token(
        confirm_token=str(confirm_token_in.confirm_token)
    )
    if not sportsman_data_out:
        raise HTTPException(status_code=status.HTTP_410_GONE)

    await auth_service.set_check_confirm_email(email=sportsman_data_out.email)

    return schemas.SportsmanEmailConfirmOut(
        email=sportsman_data_out.email,
        sport_type=sportsman_data_out.sport_type,
        trainer_id=sportsman_data_out.trainer_id,
    )


@router(
    response_model=schemas.SportsmanOut,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register_sportsman(
    register_in: schemas.SportsmanRegisterIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    sportsman_out = await sportsmans_service.get_by_email(email=register_in.email)
    if sportsman_out:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Sportsman with email {register_in.email} already exists",
        )

    is_confirmed = await auth_service.is_email_confirmed(email=register_in.email)
    if not is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Sportsman email {register_in.email} not confirmed",
        )

    team_out = await teams_service.get_by_trainer_id(trainer_id=register_in.trainer_id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Team must exist",
        )

    new_sportsman_out = await sportsmans_service.create(
        schema_in=schemas.CreateSportsmanIn(
            team_id=team_out.id,
            email=register_in.email,
            password=register_in.password,
            last_name=register_in.last_name,
            first_name=register_in.first_name,
            middle_name=register_in.middle_name,
        )
    )
    return new_sportsman_out
