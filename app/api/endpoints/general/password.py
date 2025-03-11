from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.cache.actions.auth.reset_password import ResetPasswordAction
from app.conf.settings import settings
from app.containers import Containers
from app.models import Sportsmans, Trainers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    status_code=status.HTTP_202_ACCEPTED,
)
@inject
async def send_confirm_password(
    send_pass_in: schemas.SendPasswordIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    trainer_service: Services.trainers = Depends(Provide[Containers.trainers.service]),
    sportsmans_service: Services.trainers = Depends(
        Provide[Containers.sportsmans.service]
    ),
) -> Any:
    is_blocked = await auth_service.is_email_sended(send_pass_in.email)

    if is_blocked:
        timer = await auth_service.get_email_block_timer(email=send_pass_in.email)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"detail": "email", "expire": timer},
        )

    trainer_out = await trainer_service.get_by_email(email=send_pass_in.email)
    sportsman_out = await sportsmans_service.get_by_email(email=send_pass_in.email)
    if not trainer_out and not sportsman_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if settings.DEBUG:
        confirmation_uri = await auth_service.create_reset_password_uri(
            email=send_pass_in.email
        )
        await auth_service.set_email_sended(email=send_pass_in.email)

        return {"uri": confirmation_uri, "expire": ResetPasswordAction.timeout}

    await auth_service.send_reset_password(email=send_pass_in.email)
    await auth_service.set_email_sended(email=send_pass_in.email)

    return {"expire": ResetPasswordAction.timeout}


@router(
    response_model=schemas.PasswordConfirmOut,
    status_code=status.HTTP_200_OK,
)
@inject
async def confirm_password(
    confirm_token_in: schemas.ConfirmTokenIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
) -> Any:
    data_out = await auth_service.get_reset_password_data_by_confirm_token(
        confirm_token=str(confirm_token_in.confirm_token)
    )
    if not data_out:
        raise HTTPException(status_code=status.HTTP_410_GONE)

    await auth_service.set_check_confirm_email(email=data_out.email)

    return schemas.PasswordConfirmOut(email=data_out.email)


@router(
    response_model=schemas.ClientOut,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def reset_password(
    password_in: schemas.ResetPasswordIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    trainers_service: Services.trainers = Depends(
        Provide[Containers.trainers.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
) -> Any:
    is_confirmed = await auth_service.is_email_confirmed(email=password_in.email)
    if not is_confirmed:
        raise HTTPException(status_code=status.HTTP_423_LOCKED)

    await auth_service.reset_email_confirm(email=password_in.email)

    trainer_out = await trainers_service.get_by_email(email=password_in.email)
    sportsman_out = await sportsmans_service.get_by_email(email=password_in.email)

    new_client_out: Trainers | Sportsmans
    if trainer_out:
        new_client_out = await trainers_service.update_password(
            id=trainer_out.id,
            schema_in=schemas.UpdateTrainerPasswordIn(
                password=password_in.password,
            ),
        )
        return new_client_out

    if sportsman_out:
        new_client_out = await sportsmans_service.update_password(
            id=sportsman_out.id,
            schema_in=schemas.UpdateSportsmanPasswordIn(
                password=password_in.password,
            ),
        )
        return new_client_out

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
