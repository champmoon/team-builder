from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.cache.actions.auth.confirm_email import ConfirmEmailAction
from app.conf.settings import settings
from app.consts.users_types import UsersTypes
from app.containers import Containers
from app.models import Sportsmans, Trainers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    status_code=status.HTTP_202_ACCEPTED,
)
@inject
async def send_confirm_email(
    send_email_in: schemas.SendEmailIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    trainer_service: Services.trainers = Depends(Provide[Containers.trainers.service]),
    sportsmans_service: Services.trainers = Depends(
        Provide[Containers.sportsmans.service]
    ),
) -> Any:
    is_blocked = await auth_service.is_email_sended(send_email_in.email)

    if is_blocked:
        timer = await auth_service.get_email_block_timer(email=send_email_in.email)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"detail": "email", "expire": timer},
        )

    if send_email_in.user_type == UsersTypes.TRAINER:
        trainer_out = await trainer_service.get_by_email(email=send_email_in.email)
        if trainer_out:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="trainer")

    sportsman_out = await sportsmans_service.get_by_email(email=send_email_in.email)
    if sportsman_out:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

    if settings.DEBUG:
        confirmation_uri = await auth_service.create_confirmation_url(
            confirm_data=send_email_in
        )
        await auth_service.set_email_sended(email=send_email_in.email)

        return {"uri": confirmation_uri, "expire": ConfirmEmailAction.timeout}

    await auth_service.send_confirmation_email(confirm_data=send_email_in)
    await auth_service.set_email_sended(email=send_email_in.email)

    return {"expire": ConfirmEmailAction.timeout}


@router(
    response_model=schemas.EmailConfirmOut,
    status_code=status.HTTP_200_OK,
)
@inject
async def confirm_email(
    confirm_token_in: schemas.ConfirmTokenIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
) -> Any:
    data_out = await auth_service.get_data_by_confirm_token(
        confirm_token=str(confirm_token_in.confirm_token)
    )
    if not data_out:
        raise HTTPException(status_code=status.HTTP_410_GONE)

    await auth_service.set_check_confirm_email(email=data_out.email)

    return schemas.EmailConfirmOut(email=data_out.email)


@router(
    response_model=schemas.ClientOut,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register(
    register_in: schemas.RegisterIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    trainers_service: Services.trainers = Depends(
        Provide[Containers.trainers.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    exercises_types_service: Services.exercises_types = Depends(
        Provide[Containers.exercises_types.service],
    ),
) -> Any:
    data_out = await auth_service.get_get_data_by_confirm_token(
        email=str(register_in.email)
    )
    if not data_out:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    is_confirmed = await auth_service.is_email_confirmed(email=register_in.email)
    if not is_confirmed:
        raise HTTPException(status_code=status.HTTP_423_LOCKED)

    await auth_service.reset_email_confirm(email=register_in.email)

    new_client_out: Trainers | Sportsmans
    if data_out.user_type == UsersTypes.TRAINER:
        trainer_out = await trainers_service.get_by_email(email=register_in.email)
        if trainer_out:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="trainer",
            )

        new_client_out = await trainers_service.create(
            schema_in=schemas.CreateTrainerIn(
                email=register_in.email,
                password=register_in.password,
            )
        )
        await teams_service.create(
            schema_in=schemas.CreateTeamIn(
                trainer_id=new_client_out.id,
            ),
        )

        await exercises_types_service.initialize_defaults(trainer_id=new_client_out.id)

        return new_client_out

    sportsman_out = await sportsmans_service.get_by_email(email=register_in.email)
    if sportsman_out:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

    new_client_out = await sportsmans_service.create(
        schema_in=schemas.CreateSportsmanIn(
            email=register_in.email,
            password=register_in.password,
        )
    )
    return new_client_out
