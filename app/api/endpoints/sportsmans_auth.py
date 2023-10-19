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
    response_model=schemas.SportsmanOut,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register(
    register_sportmans_in: schemas.RegisterSportsmenIn,
    sportmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service]
    ),
) -> Any:
    sportsman_out = await sportmans_service.get_by_email(
        email=register_sportmans_in.email
    )
    if sportsman_out:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Sportsman with email {register_sportmans_in.email} already exists",
        )
    return await sportmans_service.create(
        schema_in=schemas.CreateSportsmanIn(**register_sportmans_in.model_dump())
    )


@router(
    response_model=schemas.TokensOut,
    status_code=status.HTTP_200_OK,
)
@inject
async def login(
    login_sportmans_in: schemas.LoginSportsmenIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    sportmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service]
    ),
    session_service: Services.sessions = Depends(Provide[Containers.sessions.service]),
) -> Any:
    sportsman_out = await sportmans_service.get_by_email(email=login_sportmans_in.email)
    if not sportsman_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sportsman with email {login_sportmans_in.email} not found",
        )

    is_match_passwords = await auth_service.is_match_passwords(
        login_password=login_sportmans_in.password,
        hashed_password=sportsman_out.hashed_password,
    )
    if not is_match_passwords:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sportsman password didn't match",
        )

    session_out = await session_service.create(user_id=sportsman_out.id)

    return await auth_service.create_tokens(
        tokens_data=schemas.TokensEncodedSchema(
            user_id=str(sportsman_out.id),
            user_type=UsersTypes.SPORTSMAN,
        ),
        refresh_token=session_out.refresh_token,
    )


@router(
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
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
    sportmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service]
    ),
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

    sportsman_out = await sportmans_service.get_by_id(id=session_out.user_id)
    if not sportsman_out:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    await session_service.delete_by_refresh_token(
        refresh_token=session_out.refresh_token
    )

    if session_service.is_refresh_token_expired(created_at=session_out.created_at):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token expired"
        )

    new_session_out = await session_service.create(user_id=sportsman_out.id)

    return await auth_service.create_tokens(
        tokens_data=schemas.TokensEncodedSchema(
            user_id=str(new_session_out.id),
            user_type=UsersTypes.SPORTSMAN,
        ),
        refresh_token=session_out.refresh_token,
    )


@router(
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.SPORTSMAN])
@inject
async def verify() -> Response:
    return Response(status_code=status.HTTP_200_OK)
