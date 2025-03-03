from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.api import deps
from app.cache.actions import ConfirmTrainerEmailAction
from app.conf.settings import settings
from app.consts import SportsTypes, UsersTypes
from app.containers import Containers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    status_code=status.HTTP_202_ACCEPTED,
)
# @deps.auth_required(users=[UsersTypes.ADMIN])
@inject
async def send_confirm_trainer_email(
    trainer_email_confirm_in: schemas.SendTrainerEmailIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    trainer_service: Services.trainers = Depends(Provide[Containers.trainers.service]),
) -> Any:
    is_blocked = await auth_service.is_email_sended(trainer_email_confirm_in.email)

    if is_blocked:
        timer = await auth_service.get_email_block_timer(
            email=trainer_email_confirm_in.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"detail": "email", "expire": timer},
        )

    trainer_out = await trainer_service.get_by_email(
        email=trainer_email_confirm_in.email
    )
    if trainer_out:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="trainer")

    if settings.DEBUG:
        confirmation_uri = await auth_service.create_trainer_confirmation_uri(
            confirm_data=trainer_email_confirm_in
        )
        await auth_service.set_email_sended(email=trainer_email_confirm_in.email)

        return {"uri": confirmation_uri, "expire": ConfirmTrainerEmailAction.timeout}

    await auth_service.send_trainer_confirmation_email(
        confirm_data=trainer_email_confirm_in
    )
    await auth_service.set_email_sended(email=trainer_email_confirm_in.email)

    return {"expire": ConfirmTrainerEmailAction.timeout}


@router(
    response_model=schemas.TrainerEmailConfirmOut,
    status_code=status.HTTP_200_OK,
)
@inject
async def confirm_trainer_email(
    confirm_token_in: schemas.ConfirmTokenIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
) -> Any:
    trainer_data_out = await auth_service.get_trainer_data_by_confirm_token(
        confirm_token=str(confirm_token_in.confirm_token)
    )
    if not trainer_data_out:
        raise HTTPException(status_code=status.HTTP_410_GONE)

    await auth_service.set_check_confirm_email(email=trainer_data_out.email)

    return schemas.TrainerEmailConfirmOut(
        email=trainer_data_out.email,
        # first_name=trainer_data_out.first_name,
        # middle_name=trainer_data_out.middle_name,
        # last_name=trainer_data_out.last_name,
        # team_name=trainer_data_out.team_name,
        # sport_type=trainer_data_out.sport_type,
    )


@router(
    response_model=schemas.TrainerOut,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register_trainer(
    register_in: schemas.TrainerRegisterIn,
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    trainers_service: Services.trainers = Depends(
        Provide[Containers.trainers.service],
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    # team_surveys_service: Services.team_surveys = Depends(
    #     Provide[Containers.team_surveys.service],
    # ),
    exercises_types_service: Services.exercises_types = Depends(
        Provide[Containers.exercises_types.service],
    ),
) -> Any:
    trainer_out = await trainers_service.get_by_email(email=register_in.email)
    if trainer_out:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="trainer",
        )

    is_confirmed = await auth_service.is_email_confirmed(email=register_in.email)
    if not is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="trainer",
        )

    new_trainer_out = await trainers_service.create(
        schema_in=schemas.CreateTrainerIn(
            email=register_in.email,
            password=register_in.password,
            last_name=register_in.last_name,
            first_name=register_in.first_name,
            middle_name=register_in.middle_name,
        )
    )
    await teams_service.create(
        schema_in=schemas.CreateTeamIn(
            trainer_id=new_trainer_out.id,
            # name=register_in.team_name,
            # sport_type=register_in.sport_type,
        ),
    )

    # TODO: disable-surveys.md
    # await team_surveys_service.create(
    #     team_id=new_team_out.id,
    #     sport_type=SportsTypes(new_team_out.sport_type),
    # )

    await exercises_types_service.initialize_defaults(trainer_id=new_trainer_out.id)

    return new_trainer_out
