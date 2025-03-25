from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.api import deps
from app.cache.actions.auth.invite import InviteAction
from app.conf.settings import settings
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Trainers
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@router(
    response_model=schemas.TeamOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_self_team(
    self_trainer: Trainers = Depends(deps.self_trainer),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if team_out:
        return team_out
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="_team must exist",
    )


@router(
    response_model=schemas.TeamOut,
    status_code=status.HTTP_200_OK,
    deprecated=True,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def update_team_name(
    name: str,
    self_trainer: Trainers = Depends(deps.self_trainer),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    await teams_service.update_name(id=team_out.id, name=name)


@router(
    status_code=status.HTTP_202_ACCEPTED,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def send_invite_sportsman_to_team(
    invite_sportsman_in: schemas.InviteSportsmanToTeamIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
) -> Any:
    is_blocked = await auth_service.is_email_sended(invite_sportsman_in.email)

    if is_blocked:
        timer = await auth_service.get_email_block_timer(
            email=invite_sportsman_in.email
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"detail": "email", "expire": timer},
        )

    sportsman_email = invite_sportsman_in.email

    sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
    if not sportsman_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    if sportsman_out.team_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

    if settings.DEBUG:
        confirmation_uri = await auth_service.create_invite_url(
            team_id=team_out.id, fake_id=invite_sportsman_in.local_sportsman_id
        )
        await auth_service.set_email_sended(email=sportsman_email)

        return {"uri": confirmation_uri, "expire": InviteAction.timeout}

    await auth_service.send_invite_email(
        team_id=team_out.id,
        sportsman_email=sportsman_email,
        fake_id=invite_sportsman_in.local_sportsman_id,
    )
    await auth_service.set_email_sended(email=sportsman_email)

    return {"expire": InviteAction.timeout}


@router(
    response_model=schemas.TeamInviteLink,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_invite_link(
    self_trainer: Trainers = Depends(deps.self_trainer),
    auth_service: Services.auth = Depends(Provide[Containers.auth.service]),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    link = await auth_service.create_invite_url(team_id=team_out.id)
    return schemas.TeamInviteLink(link=link)


@router(
    response_model=schemas.TeamOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def kicks_sportsmans_off_team(
    sportsmans_emails_in: schemas.ListSportsmansEmailsIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_team must exist",
        )

    sportsmans_emails = sportsmans_emails_in.sportsmans_emails
    for sportsman_email in sportsmans_emails:
        sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
        if not sportsman_out:
            continue

        if sportsman_out.team_id != team_out.id:
            continue

        await sportsmans_service.kick_off_team(sportsman_id=sportsman_out.id)

        sportsmans_groups = (
            await sportsmans_groups_service.get_all_groups_by_sportsman_id(
                sportsman_id=sportsman_out.id
            )
        )
        for sportsman_group in sportsmans_groups:
            await sportsmans_groups_service.delete(
                schema_in=schemas.DeleteSportsmanGroupIn(
                    sportsman_id=sportsman_out.id,
                    group_id=sportsman_group.group_id,
                )
            )
            future_group_workouts_ids = (
                await tgs_workouts_service.get_future_group_workouts_ids(
                    group_id=sportsman_group.group_id
                )
            )
            await sportsmans_workouts_service.unbind_sportsman_to_workouts(
                sportsman_id=sportsman_out.id,
                workouts_ids=future_group_workouts_ids,
            )

        future_team_workouts_ids = (
            await tgs_workouts_service.get_future_team_workouts_ids(team_id=team_out.id)
        )
        await sportsmans_workouts_service.unbind_sportsman_to_workouts(
            sportsman_id=sportsman_out.id,
            workouts_ids=future_team_workouts_ids,
        )

    return await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)


# @router(
#     response_model=schemas.TeamOut,
#     status_code=status.HTTP_200_OK,
# )
# @deps.auth_required(users=[UsersTypes.TRAINER])
# @inject
# async def adds_sportsmans_to_team(
#     sportsmans_emails_in: schemas.ListSportsmansEmailsIn,
#     self_trainer: Trainers = Depends(deps.self_trainer),
#     teams_service: Services.teams = Depends(
#         Provide[Containers.teams.service],
#     ),
#     sportsmans_service: Services.sportsmans = Depends(
#         Provide[Containers.sportsmans.service],
#     ),
# ) -> Any:
#     team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
#     if not team_out:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="_team must exist",
#         )

#     sportsman_emails = sportsmans_emails_in.sportsmans_emails
#     for sportsman_email in sportsman_emails:
#         sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
#         if not sportsman_out:
#             continue

#         if sportsman_out.team_id == team_out.id:
#             continue

#         await sportsmans_service.add_to_team(
#             sportsman_id=sportsman_out.id,
#             team_id=team_out.id,
#         )

#     return await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)


# @router(
#     response_model=schemas.TeamOut,
#     status_code=status.HTTP_200_OK,
# )
# @deps.auth_required(users=[UsersTypes.TRAINER])
# @inject
# async def kick_sportsman_off_team(
#     sportsman_email_in: schemas.SportsmansEmailIn,
#     self_trainer: Trainers = Depends(deps.self_trainer),
#     teams_service: Services.teams = Depends(
#         Provide[Containers.teams.service],
#     ),
#     sportsmans_service: Services.sportsmans = Depends(
#         Provide[Containers.sportsmans.service],
#     ),
#     sportsmans_groups_service: Services.sportsmans_groups = Depends(
#         Provide[Containers.sportsmans_groups.service],
#     ),
# ) -> Any:
#     sportsman_email = sportsman_email_in.sportsman_email

#     sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
#     if not sportsman_out:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sportsman")

#     team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
#     if not team_out:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="_team must exist",
#         )

#     if sportsman_out.team_id != team_out.id:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

#     await sportsmans_service.kick_off_team(sportsman_id=sportsman_out.id)

#     sportsmans_groups = (
#         await sportsmans_groups_service.get_all_groups_by_sportsman_id(
#             sportsman_id=sportsman_out.id
#         )
#     )
#     for sportsman_group in sportsmans_groups:
#         await sportsmans_groups_service.delete(
#             schema_in=schemas.DeleteSportsmanGroupIn(
#                 sportsman_id=sportsman_out.id,
#                 group_id=sportsman_group.group_id,
#             )
#         )

#     return await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
