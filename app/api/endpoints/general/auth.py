from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, Response, status

from app import schemas
from app.api import deps
from app.cache.actions.auth.confirm_email import ConfirmEmailAction
from app.conf.settings import settings
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Admins, Sportsmans, Trainers
from app.services import Services
from app.utils import UsersScope
from app.utils.jwt import JWTManager
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
                    status_code=status.HTTP_404_NOT_FOUND, detail="user"
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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user")

    session_out = await session_service.create(
        user_id=user_out.id, user_type=user_type, remember_me=login_in.remember_me
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
            detail="refresh_token",
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
            detail="refresh_token",
        )

    await session_service.delete_by_refresh_token(
        refresh_token=session_out.refresh_token
    )

    if session_service.is_refresh_token_expired(
        created_at=session_out.created_at,
        remember_me=session_out.remember_me,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="refresh_token",
        )

    new_session_out = await session_service.create(
        user_id=session_out.user_id,
        user_type=session_out.user_type,
        remember_me=session_out.remember_me,
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
    response_model=schemas.VerifyResponse,
)
# @deps.auth_required(users=UsersScope.all())
@inject
async def verify(
    access_data_in: schemas.AccessTokenIn,
) -> Any:
    jwt_manager = JWTManager()
    token_data = jwt_manager.decode_access_token(access_data_in.access_token)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return schemas.VerifyResponse(user_type=token_data.user_type)


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

    if send_email_in.is_trainer:
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

    new_client_out: Trainers | Sportsmans
    if data_out.is_trainer:
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
