# from typing import Any
# from uuid import UUID

# from dependency_injector.wiring import Provide, inject
# from fastapi import Depends, HTTPException, status

# from app import consts, schemas
# from app.api import deps
# from app.consts import UsersTypes, WorkoutsStatusesEnum
# from app.containers import Containers
# from app.models import Sportsmans, SportsmansWorkouts, Workouts
# from app.services import Services
# from app.utils.router import EndPointRouter

# router = EndPointRouter()


# @inject
# async def get_workout_schema(
#     workout_out: Workouts,
#     sportsman_workout_out: SportsmansWorkouts,
#     tgs_workouts_service: Services.tgs_workouts = Depends(
#         Provide[Containers.tgs_workouts.service]
#     ),
# ) -> (
#     schemas.SportsmansSportsmanWorkoutOut
#     | schemas.SportsmansGroupWorkoutOut
#     | schemas.SportsmansTeamWorkoutOut
# ):
#     base_workouts_schemas = schemas.TrainerWorkoutOut(
#         id=workout_out.id,
#         name=workout_out.workout_pool.name,
#         estimated_time=workout_out.workout_pool.estimated_time,
#         status=schemas.WorkoutsStatusesOut(
#             status=consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status),
#             description=consts.WORKOUTS_STATUSES_DESC[
#                 consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status)
#             ],
#         ),
#         date=workout_out.date,
#         created_at=workout_out.workout_pool.created_at,
#         exercises=workout_out.workout_pool.exercises,
#         rest_time=workout_out.rest_time,
#         price=workout_out.price,
#         comment=workout_out.comment,
#         goal=workout_out.goal,
#         repeat_id=workout_out.repeat_id,
#     )

#     tgs_workouts_out = await tgs_workouts_service.get_by_workout_id(
#         workout_id=sportsman_workout_out.workout_id
#     )
#     if not tgs_workouts_out:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="_workout not found in tgs",
#         )

#     workout_schema: (
#         schemas.SportsmansSportsmanWorkoutOut
#         | schemas.SportsmansGroupWorkoutOut
#         | schemas.SportsmansTeamWorkoutOut
#     )
#     team_id = tgs_workouts_out.team_id
#     group_id = tgs_workouts_out.group_id
#     sportsman_id = tgs_workouts_out.sportsman_id
#     if team_id:
#         workout_schema = schemas.SportsmansTeamWorkoutOut(
#             **base_workouts_schemas.model_dump(),
#             team_id=team_id,
#         )
#     elif group_id:
#         workout_schema = schemas.SportsmansGroupWorkoutOut(
#             **base_workouts_schemas.model_dump(),
#             group_id=group_id,
#         )
#     elif sportsman_id:
#         workout_schema = schemas.SportsmansSportsmanWorkoutOut(
#             **base_workouts_schemas.model_dump(),
#             sportsman_id=sportsman_id,
#         )
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="_tgs all none ids",
#         )

#     return workout_schema


# @inject
# async def get_self_trainer_id(
#     sportsman_out: Sportsmans,
#     teams_service: Services.teams = Depends(
#         Provide[Containers.teams.service],
#     ),
# ) -> UUID:
#     if not sportsman_out.team_id:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="sportsman_team"
#         )

#     team_out = await teams_service.get_by_id(id=sportsman_out.team_id)
#     if not team_out:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="sportsman_team"
#         )
#     return team_out.trainer_id


# @router(
#     response_model=(
#         schemas.SportsmansSportsmanWorkoutOut
#         | schemas.SportsmansGroupWorkoutOut
#         | schemas.SportsmansTeamWorkoutOut
#     ),
#     status_code=status.HTTP_200_OK,
# )
# @deps.auth_required(users=[UsersTypes.SPORTSMAN])
# @inject
# async def start_workout(
#     id: UUID,
#     self_sportsman: Sportsmans = Depends(deps.self_sportsman),
#     workouts_service: Services.workouts = Depends(
#         Provide[Containers.workouts.service],
#     ),
#     sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
#         Provide[Containers.sportsmans_workouts.service]
#     ),
#     trainers_workouts_service: Services.trainers_workouts = Depends(
#         Provide[Containers.trainers_workouts.service]
#     ),
# ) -> Any:
#     workout_out = await workouts_service.get_by_id(id=id)
#     if not workout_out:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

#     sportsman_workout_out = await sportsmans_workouts_service.get_by(
#         workout_id=workout_out.id, sportsman_id=self_sportsman.id
#     )
#     if not sportsman_workout_out:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

#     if (
#         WorkoutsStatusesEnum(sportsman_workout_out.status.status)
#         != WorkoutsStatusesEnum.ACTIVE
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="workout_status",
#         )

#     sportsman_workout_out = await sportsmans_workouts_service.in_progress(
#         schema_in=schemas.UpdateSportsmansWorkoutIn(
#             sportsman_id=self_sportsman.id,
#             workout_id=workout_out.id,
#         )
#     )

#     other_sportsmans_workouts_out = (
#         await sportsmans_workouts_service.get_other_by_statuses(
#             workout_id=id,
#             self_sportsman_id=self_sportsman.id,
#             statuses=(WorkoutsStatusesEnum.IN_PROGRESS,),
#         )
#     )
#     if len(other_sportsmans_workouts_out) == 0:
#         await trainers_workouts_service.in_progress(
#             schema_in=schemas.UpdateTrainerWorkoutIn(
#                 workout_id=id,
#                 trainer_id=await get_self_trainer_id(sportsman_out=self_sportsman),
#             )
#         )

#     return await get_workout_schema(
#         workout_out=workout_out, sportsman_workout_out=sportsman_workout_out
#     )


# @router(
#     response_model=(
#         schemas.SportsmansSportsmanWorkoutOut
#         | schemas.SportsmansGroupWorkoutOut
#         | schemas.SportsmansTeamWorkoutOut
#     ),
#     status_code=status.HTTP_200_OK,
# )
# @deps.auth_required(users=[UsersTypes.SPORTSMAN])
# @inject
# async def complete_workout(
#     id: UUID,
#     self_sportsman: Sportsmans = Depends(deps.self_sportsman),
#     workouts_service: Services.workouts = Depends(
#         Provide[Containers.workouts.service],
#     ),
#     sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
#         Provide[Containers.sportsmans_workouts.service]
#     ),
#     stress_questionnaires_service: Services.stress_questionnaires = Depends(
#         Provide[Containers.stress_questionnaires.service],
#     ),
#     health_questionnaires_service: Services.health_questionnaires = Depends(
#         Provide[Containers.health_questionnaires.service],
#     ),
#     trainers_workouts_service: Services.trainers_workouts = Depends(
#         Provide[Containers.trainers_workouts.service]
#     ),
# ) -> Any:
#     workout_out = await workouts_service.get_by_id(id=id)
#     if not workout_out:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

#     sportsman_workout_out = await sportsmans_workouts_service.get_by(
#         workout_id=workout_out.id, sportsman_id=self_sportsman.id
#     )
#     if not sportsman_workout_out:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

#     if (
#         WorkoutsStatusesEnum(sportsman_workout_out.status.status)
#         != WorkoutsStatusesEnum.IN_PROGRESS
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="workout_status",
#         )

#     sportsman_workout_out = await sportsmans_workouts_service.completed(
#         schema_in=schemas.UpdateSportsmansWorkoutIn(
#             sportsman_id=self_sportsman.id,
#             workout_id=workout_out.id,
#         )
#     )

#     all_sportsmans_len = len(
#         await sportsmans_workouts_service.get_all_by_workout_id(workout_id=id)
#     )
#     other_sportsmans_len = len(
#         await sportsmans_workouts_service.get_other_by_statuses(
#             workout_id=id,
#             self_sportsman_id=self_sportsman.id,
#             statuses=(WorkoutsStatusesEnum.COMPLETED, WorkoutsStatusesEnum.CANCELED),
#         )
#     )

#     if other_sportsmans_len == all_sportsmans_len - 1:
#         await trainers_workouts_service.completed(
#             schema_in=schemas.UpdateTrainerWorkoutIn(
#                 workout_id=id,
#                 trainer_id=await get_self_trainer_id(sportsman_out=self_sportsman),
#             )
#         )

#     workout_schema = await get_workout_schema(
#         workout_out=workout_out,
#         sportsman_workout_out=sportsman_workout_out,
#     )

#     await stress_questionnaires_service.create(
#         schema_in=schemas.CreateStressQuestionnaireIn(
#             sportsman_id=self_sportsman.id,
#             workout_id=workout_out.id,
#         ),
#         timeout=workout_out.price,
#     )

#     await health_questionnaires_service.set_on_next_day(
# sportsman_id=self_sportsman.id)

#     return workout_schema


# @router(
#     response_model=(
#         schemas.SportsmansSportsmanWorkoutOut
#         | schemas.SportsmansGroupWorkoutOut
#         | schemas.SportsmansTeamWorkoutOut
#     ),
#     status_code=status.HTTP_200_OK,
# )
# @deps.auth_required(users=[UsersTypes.SPORTSMAN])
# @inject
# async def cancel_workout(
#     id: UUID,
#     self_sportsman: Sportsmans = Depends(deps.self_sportsman),
#     workouts_service: Services.workouts = Depends(
#         Provide[Containers.workouts.service],
#     ),
#     sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
#         Provide[Containers.sportsmans_workouts.service]
#     ),
#     stress_questionnaires_service: Services.stress_questionnaires = Depends(
#         Provide[Containers.stress_questionnaires.service],
#     ),
#     health_questionnaires_service: Services.health_questionnaires = Depends(
#         Provide[Containers.health_questionnaires.service],
#     ),
#     trainers_workouts_service: Services.trainers_workouts = Depends(
#         Provide[Containers.trainers_workouts.service]
#     ),
# ) -> Any:
#     workout_out = await workouts_service.get_by_id(id=id)
#     if not workout_out:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

#     sportsman_workout_out = await sportsmans_workouts_service.get_by(
#         workout_id=workout_out.id, sportsman_id=self_sportsman.id
#     )
#     if not sportsman_workout_out:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

#     if (
#         WorkoutsStatusesEnum(sportsman_workout_out.status.status)
#         != WorkoutsStatusesEnum.IN_PROGRESS
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="workout_status",
#         )

#     sportsman_workout_out = await sportsmans_workouts_service.canceled(
#         schema_in=schemas.UpdateSportsmansWorkoutIn(
#             sportsman_id=self_sportsman.id,
#             workout_id=workout_out.id,
#         )
#     )

#     all_sportsmans_len = len(
#         await sportsmans_workouts_service.get_all_by_workout_id(workout_id=id)
#     )
#     canceled_sportsmans_len = len(
#         await sportsmans_workouts_service.get_other_by_statuses(
#             workout_id=id,
#             self_sportsman_id=self_sportsman.id,
#             statuses=(WorkoutsStatusesEnum.CANCELED,),
#         )
#     )
#     completed_sportsmans_len = len(
#         await sportsmans_workouts_service.get_other_by_statuses(
#             workout_id=id,
#             self_sportsman_id=self_sportsman.id,
#             statuses=(WorkoutsStatusesEnum.COMPLETED,),
#         )
#     )

#     if canceled_sportsmans_len == all_sportsmans_len - 1:
#         await trainers_workouts_service.canceled(
#             schema_in=schemas.UpdateTrainerWorkoutIn(
#                 workout_id=id,
#                 trainer_id=await get_self_trainer_id(sportsman_out=self_sportsman),
#             )
#         )
#     elif canceled_sportsmans_len + completed_sportsmans_len == all_sportsmans_len - 1:
#         await trainers_workouts_service.completed(
#             schema_in=schemas.UpdateTrainerWorkoutIn(
#                 workout_id=id,
#                 trainer_id=await get_self_trainer_id(sportsman_out=self_sportsman),
#             )
#         )

#     workout_schema = await get_workout_schema(
#         workout_out=workout_out,
#         sportsman_workout_out=sportsman_workout_out,
#     )

#     await stress_questionnaires_service.create(
#         schema_in=schemas.CreateStressQuestionnaireIn(
#             sportsman_id=self_sportsman.id,
#             workout_id=workout_out.id,
#         ),
#         timeout=workout_out.price,
#     )

#     await health_questionnaires_service.set_on_next_day(
# sportsman_id=self_sportsman.id)

#     return workout_schema
