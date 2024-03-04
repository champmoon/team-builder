from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Response, status

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Admins, Sportsmans, Trainers
from app.services import Services
from app.utils import UsersScope
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.TokensOut,
    status_code=status.HTTP_200_OK,
)
@inject
async def login(
    login_in: schemas.LoginIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    sportmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service]
    ),
    trainers_service: Services.trainers = Depends(
        Provide[Containers.trainers.service],
    ),
    admins_service: Services.admins = Depends(
        Provide[Containers.admins.service],
    ),
    session_service: Services.sessions = Depends(Provide[Containers.sessions.service]),
) -> Any:
    user_out: Trainers | Sportsmans | Admins

    sportsman_out = await sportmans_service.get_by_email(email=login_in.email)
    if not sportsman_out:
        trainer_out = await trainers_service.get_by_email(email=login_in.email)
        if not trainer_out:
            admin_out = await admins_service.get_by_email(email=login_in.email)
            if not admin_out:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with email {login_in.email} not found",
                )

            user_out = admin_out
            user_type = UsersTypes.ADMIN
        else:
            user_out = trainer_out
            user_type = UsersTypes.TRAINER
    else:
        user_out = sportsman_out
        user_type = UsersTypes.SPORTSMAN

    is_match_passwords = await auth_service.is_match_passwords(
        login_password=login_in.password,
        hashed_password=user_out.hashed_password,
    )
    if not is_match_passwords:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User password didn't match",
        )

    session_out = await session_service.create(
        user_id=user_out.id,
        user_type=user_type,
    )
    return await auth_service.create_tokens(
        tokens_data=schemas.TokensEncodedSchema(
            user_id=str(user_out.id),
            user_type=user_type,
        ),
        refresh_token=session_out.refresh_token,
    )


@router(
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=UsersScope.all())
@inject
async def logout(
    refresh_data_in: schemas.RefreshTokenIn,
    session_service: Services.sessions = Depends(Provide[Containers.sessions.service]),
) -> Response:
    session_out = await session_service.get_by_refresh_token(
        refresh_token=refresh_data_in.refresh_token
    )
    if not session_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found",
        )

    await session_service.delete_by_refresh_token(
        refresh_token=session_out.refresh_token
    )
    return Response(status_code=status.HTTP_200_OK)


@router(
    response_model=schemas.TokensOut,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def refresh(
    refresh_data_in: schemas.RefreshTokenIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    session_service: Services.sessions = Depends(Provide[Containers.sessions.service]),
) -> Any:
    session_out = await session_service.get_by_refresh_token(
        refresh_token=refresh_data_in.refresh_token
    )
    if not session_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found",
        )

    await session_service.delete_by_refresh_token(
        refresh_token=session_out.refresh_token
    )

    if session_service.is_refresh_token_expired(created_at=session_out.created_at):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token expired",
        )

    new_session_out = await session_service.create(
        user_id=session_out.user_id,
        user_type=session_out.user_type,
    )

    return await auth_service.create_tokens(
        tokens_data=schemas.TokensEncodedSchema(
            user_id=str(new_session_out.user_id),
            user_type=session_out.user_type,
        ),
        refresh_token=new_session_out.refresh_token,
    )


@router(
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=UsersScope.all())
@inject
async def verify() -> Response:
    return Response(status_code=status.HTTP_200_OK)
