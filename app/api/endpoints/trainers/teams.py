from typing import Any

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import schemas
from app.api import deps
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


# @router(
#     response_model=schemas.TeamOut,
#     status_code=status.HTTP_200_OK,
# )
# @deps.auth_required(users=[UsersTypes.TRAINER])
# @inject
# async def add_sportsman_to_team(
#     sportsman_email_in: schemas.SportsmansEmailIn,
#     self_trainer: Trainers = Depends(deps.self_trainer),
#     teams_service: Services.teams = Depends(
#         Provide[Containers.teams.service],
#     ),
#     sportsmans_service: Services.sportsmans = Depends(
#         Provide[Containers.sportsmans.service],
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

#     if sportsman_out.team_id:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="sportsman")

#     await sportsmans_service.add_to_team(
#         sportsman_id=sportsman_out.id,
#         team_id=team_out.id,
#     )
#     return await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)


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


# @router(
#     response_model=schemas.TeamOut,
#     status_code=status.HTTP_200_OK,
# )
# @deps.auth_required(users=[UsersTypes.TRAINER])
# @inject
# async def kicks_sportsmans_off_team(
#     sportsmans_emails_in: schemas.ListSportsmansEmailsIn,
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
#     team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
#     if not team_out:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="_team must exist",
#         )

#     sportsmans_emails = sportsmans_emails_in.sportsmans_emails
#     for sportsman_email in sportsmans_emails:
#         sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
#         if not sportsman_out:
#             continue

#         if sportsman_out.team_id != team_out.id:
#             continue

#         await sportsmans_service.kick_off_team(sportsman_id=sportsman_out.id)

#         sportsmans_groups = (
#             await sportsmans_groups_service.get_all_groups_by_sportsman_id(
#                 sportsman_id=sportsman_out.id
#             )
#         )
#         for sportsman_group in sportsmans_groups:
#             await sportsmans_groups_service.delete(
#                 schema_in=schemas.DeleteSportsmanGroupIn(
#                     sportsman_id=sportsman_out.id,
#                     group_id=sportsman_group.group_id,
#                 )
#             )

#     return await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
