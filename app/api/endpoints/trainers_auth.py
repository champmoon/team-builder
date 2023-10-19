from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Response, status

from app import schemas
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.TrainerOut,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register(
    register_trainer_in: schemas.RegisterTrainerIn,
    trainer_service: Services.trainers = Depends(Provide[Containers.trainers.service]),
) -> Any:
    trainer_out = await trainer_service.get_by_email(email=register_trainer_in.email)
    if trainer_out:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Trainer with email {register_trainer_in.email} already exists",
        )
    return await trainer_service.create(
        schema_in=schemas.CreateTrainerIn(**register_trainer_in.model_dump())
    )


@router(
    response_model=schemas.TokensOut,
    status_code=status.HTTP_200_OK,
)
@inject
async def login(
    login_trainer_in: schemas.LoginTrainerIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    trainer_service: Services.trainers = Depends(Provide[Containers.trainers.service]),
    session_service: Services.sessions = Depends(Provide[Containers.sessions.service]),
) -> Any:
    trainer_out = await trainer_service.get_by_email(email=login_trainer_in.email)
    if not trainer_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trainer with email {login_trainer_in.email} not found",
        )

    is_match_passwords = await auth_service.is_match_passwords(
        login_password=login_trainer_in.password,
        hashed_password=trainer_out.hashed_password,
    )
    if not is_match_passwords:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Trainer password didn't match",
        )

    session_out = await session_service.create(user_id=trainer_out.id)

    return await auth_service.create_tokens(
        tokens_data=schemas.TokensEncodedSchema(
            user_id=str(trainer_out.id),
            user_type=UsersTypes.TRAINER,
        ),
        refresh_token=session_out.refresh_token,
    )


@router(
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
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
    trainer_service: Services.trainers = Depends(Provide[Containers.trainers.service]),
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

    trainer_out = await trainer_service.get_by_id(id=session_out.user_id)
    if not trainer_out:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await session_service.delete_by_refresh_token(
        refresh_token=session_out.refresh_token
    )

    if session_service.is_refresh_token_expired(created_at=session_out.created_at):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token expired"
        )

    new_session_out = await session_service.create(user_id=trainer_out.id)

    return await auth_service.create_tokens(
        tokens_data=schemas.TokensEncodedSchema(
            user_id=str(new_session_out.id),
            user_type=UsersTypes.TRAINER,
        ),
        refresh_token=session_out.refresh_token,
    )


@router(
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def verify() -> Response:
    return Response(status_code=status.HTTP_200_OK)
