from typing import Any
from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status, Response
from pydantic import TypeAdapter
from app import schemas
from app import consts
from app.api import deps
from app.consts import UsersTypes
from app.containers import Containers
from app.models import Trainers
from app.services import Services
from app.utils.router import EndPointRouter
from app.services.exercises import InvalidOrderExercisesException

router = EndPointRouter()


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_workout_for_sportsman(
    create_workout_in: schemas.CreateWorkoutForSportsmanIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
    exercises_service: Services.exercises = Depends(
        Provide[Containers.exercises.service]
    ),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    workouts_statuses_service: Services.workouts_statuses = Depends(
        Provide[Containers.workouts_statuses.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
) -> Any:
    sportsman_email = create_workout_in.sportsman_email
    sportsman_out = await sportsmans_service.get_by_email(email=sportsman_email)
    if not sportsman_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sportsman with email {sportsman_email} not found",
        )

    try:
        estimated_time = await exercises_service.count_estimated_time(
            exercises=create_workout_in.exercises
        )
        new_workout_out = await workouts_service.create(
            schema_in=schemas.CreateWorkoutInDB(
                name=create_workout_in.name,
                estimated_time=estimated_time,
                date=create_workout_in.date,
            ),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    try:
        new_exercises_schemas = await exercises_service.create(
            workout_id=new_workout_out.id,
            exercises_in=create_workout_in.exercises,
        )
    except InvalidOrderExercisesException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exercises order must be sequance as 1, 2, 3, ...",
        )
    except ValueError as e:
        await workouts_service.delete(id=new_workout_out.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    workout_status_out = await workouts_statuses_service.get_by_status(
        status=consts.WorkoutsStatusesEnum.PLANNED
    )
    if not workout_status_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Workout status not found",
        )

    await sportsmans_workouts_service.create(
        schema_in=schemas.CreateSportsmansWorkoutIn(
            sportsman_id=sportsman_out.id,
            workout_id=new_workout_out.id,
            status_id=workout_status_out.id,
        )
    )

    await trainers_workouts_service.create(
        schema_in=schemas.CreateTrainerWorkoutIn(
            trainer_id=self_trainer.id,
            workout_id=new_workout_out.id,
            status_id=workout_status_out.id,
        )
    )

    return schemas.TrainerWorkoutOut(
        workout_id=new_workout_out.id,
        name=new_workout_out.name,
        estimated_time=estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=workout_status_out.status,
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(workout_status_out.status)
            ],
        ),
        date=new_workout_out.date,
        created_at=new_workout_out.created_at,
        exercises=new_exercises_schemas,
    )


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_workout_for_group(
    create_workout_in: schemas.CreateWorkoutForGroupIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    sportsmans_groups_service: Services.sportsmans_groups = Depends(
        Provide[Containers.sportsmans_groups.service],
    ),
    exercises_service: Services.exercises = Depends(
        Provide[Containers.exercises.service]
    ),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    workouts_statuses_service: Services.workouts_statuses = Depends(
        Provide[Containers.workouts_statuses.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    groups_service: Services.groups = Depends(
        Provide[Containers.groups.service],
    ),
    teams_groups_workouts_service: Services.teams_groups_workouts = Depends(
        Provide[Containers.teams_groups_workouts.service]
    ),
) -> Any:
    group_id = create_workout_in.group_id
    group_out = await groups_service.get_by_id(id=group_id)
    if not group_out or group_out.trainer_id != self_trainer.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found",
        )

    sportsmans_out = await sportsmans_groups_service.get_all_sportsmans_by_group_id(
        group_id=group_id
    )
    if len(sportsmans_out) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The group must not be empty",
        )

    try:
        estimated_time = await exercises_service.count_estimated_time(
            exercises=create_workout_in.exercises
        )
        new_workout_out = await workouts_service.create(
            schema_in=schemas.CreateWorkoutInDB(
                name=create_workout_in.name,
                estimated_time=estimated_time,
                date=create_workout_in.date,
            ),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    try:
        new_exercises_schemas = await exercises_service.create(
            workout_id=new_workout_out.id,
            exercises_in=create_workout_in.exercises,
        )
    except InvalidOrderExercisesException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exercises order must be sequance as 1, 2, 3, ...",
        )
    except ValueError as e:
        await workouts_service.delete(id=new_workout_out.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    workout_status_out = await workouts_statuses_service.get_by_status(
        status=consts.WorkoutsStatusesEnum.PLANNED
    )
    if not workout_status_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Workout status not found",
        )

    for sportsman_out in sportsmans_out:
        await sportsmans_workouts_service.create(
            schema_in=schemas.CreateSportsmansWorkoutIn(
                sportsman_id=sportsman_out.sportsman_id,
                workout_id=new_workout_out.id,
                status_id=workout_status_out.id,
            )
        )

    await teams_groups_workouts_service.create(
        schema_in=schemas.CreateTeamGroupWorkoutIn(
            group_id=group_id,
            workout_id=new_workout_out.id,
        )
    )

    await trainers_workouts_service.create(
        schema_in=schemas.CreateTrainerWorkoutIn(
            trainer_id=self_trainer.id,
            workout_id=new_workout_out.id,
            status_id=workout_status_out.id,
        )
    )

    return schemas.TrainerWorkoutOut(
        workout_id=new_workout_out.id,
        name=new_workout_out.name,
        estimated_time=estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=workout_status_out.status,
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(workout_status_out.status)
            ],
        ),
        date=new_workout_out.date,
        created_at=new_workout_out.created_at,
        exercises=new_exercises_schemas,
    )


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_workout_for_team(
    create_workout_in: schemas.CreateWorkoutForTeamIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    exercises_service: Services.exercises = Depends(
        Provide[Containers.exercises.service]
    ),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    workouts_statuses_service: Services.workouts_statuses = Depends(
        Provide[Containers.workouts_statuses.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    teams_service: Services.teams = Depends(
        Provide[Containers.teams.service],
    ),
    teams_groups_workouts_service: Services.teams_groups_workouts = Depends(
        Provide[Containers.teams_groups_workouts.service]
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service],
    ),
) -> Any:
    team_out = await teams_service.get_by_trainer_id(trainer_id=self_trainer.id)
    if not team_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Team must exist",
        )

    sportsmans_out = await sportsmans_service.get_by_team_id(team_id=team_out.id)
    if len(sportsmans_out) == 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The team must not be empty",
        )

    try:
        estimated_time = await exercises_service.count_estimated_time(
            exercises=create_workout_in.exercises
        )
        new_workout_out = await workouts_service.create(
            schema_in=schemas.CreateWorkoutInDB(
                name=create_workout_in.name,
                estimated_time=estimated_time,
                date=create_workout_in.date,
            ),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    try:
        new_exercises_schemas = await exercises_service.create(
            workout_id=new_workout_out.id,
            exercises_in=create_workout_in.exercises,
        )
    except InvalidOrderExercisesException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exercises order must be sequance as 1, 2, 3, ...",
        )
    except ValueError as e:
        await workouts_service.delete(id=new_workout_out.id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

    workout_status_out = await workouts_statuses_service.get_by_status(
        status=consts.WorkoutsStatusesEnum.PLANNED
    )
    if not workout_status_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Workout status not found",
        )

    for sportsman_out in sportsmans_out:
        await sportsmans_workouts_service.create(
            schema_in=schemas.CreateSportsmansWorkoutIn(
                sportsman_id=sportsman_out.id,
                workout_id=new_workout_out.id,
                status_id=workout_status_out.id,
            )
        )

    await teams_groups_workouts_service.create(
        schema_in=schemas.CreateTeamGroupWorkoutIn(
            team_id=team_out.id,
            workout_id=new_workout_out.id,
        )
    )

    await trainers_workouts_service.create(
        schema_in=schemas.CreateTrainerWorkoutIn(
            trainer_id=self_trainer.id,
            workout_id=new_workout_out.id,
            status_id=workout_status_out.id,
        )
    )

    return schemas.TrainerWorkoutOut(
        workout_id=new_workout_out.id,
        name=new_workout_out.name,
        estimated_time=estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=workout_status_out.status,
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(workout_status_out.status)
            ],
        ),
        date=new_workout_out.date,
        created_at=new_workout_out.created_at,
        exercises=new_exercises_schemas,
    )


# @router(
#     response_model=list[
#         schemas.TrainerSportsmanWorkoutOut
#         | schemas.TrainerGroupWorkoutOut
#         | schemas.TrainerTeamWorkoutOut
#     ],
#     status_code=status.HTTP_200_OK,
# )
# @deps.auth_required(users=[UsersTypes.TRAINER])
# @inject
# async def get_workouts(
#     self_trainer: Trainers = Depends(deps.self_trainer),
#     exercises_service: Services.exercises = Depends(
#         Provide[Containers.exercises.service]
#     ),
#     workouts_service: Services.workouts = Depends(
#         Provide[Containers.workouts.service],
#     ),
#     workouts_statuses_service: Services.workouts_statuses = Depends(
#         Provide[Containers.workouts_statuses.service]
#     ),
#     sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
#         Provide[Containers.sportsmans_workouts.service]
#     ),
#     trainers_workouts_service: Services.trainers_workouts = Depends(
#         Provide[Containers.trainers_workouts.service]
#     ),
#     teams_service: Services.teams = Depends(
#         Provide[Containers.teams.service],
#     ),
#     teams_groups_workouts_service: Services.teams_groups_workouts = Depends(
#         Provide[Containers.teams_groups_workouts.service]
#     ),
#     sportsmans_service: Services.sportsmans = Depends(
#         Provide[Containers.sportsmans.service],
#     ),
# ) -> Any:
#     trainers_workouts_out = await trainers_workouts_service.get_all_by_trainer_id(
#         trainer_id=self_trainer.id
#     )
#     if len(trainers_workouts_out) == 0:
#         return []

#     workouts: list[
#         schemas.TrainerSportsmanWorkoutOut
#         | schemas.TrainerGroupWorkoutOut
#         | schemas.TrainerTeamWorkoutOut
#     ] = []
#     for trainer_workout_out in trainers_workouts_out:
#         workout_out = await workouts_service.get_by_id(
#             id=trainer_workout_out.workout_id
#         )
#         if not workout_out:
#             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         exercises_out = await exercises_service.get_all_exercises_by_workout_id(
#             workout_id=workout_out.id
#         )
#         exercises_schemas: list[schemas.ExerciseOut] = []
#         for exercise_out in exercises_out:
#             exercises_schemas.append(
#                 schemas.ExerciseOut(
#                     type=schemas.ExercisesTypesOut(
#                         type=exercise_out.type.type,
#                         average_time=exercise_out.type.average_time,
#                     ),
#                     reps=exercise_out.reps,
#                     sets=exercise_out.sets,
#                     rest=exercise_out.rest,
#                     time=exercise_out.time,
#                     order=exercise_out.order,
#                 )
#             )
#         base_workouts_schemas = schemas.TrainerWorkoutOut(
#             workout_id=workout_out.id,
#             name=workout_out.name,
#             estimated_time=workout_out.estimated_time,
#             status=schemas.WorkoutsStatusesOut(
#                 status=trainer_workout_out.status.status,
#                 description=consts.WORKOUTS_STATUSES_DESC[
#                     consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
#                 ],
#             ),
#             date=workout_out.date,
#             created_at=workout_out.created_at,
#             exercises=exercises_schemas,
#         )

#         teams_groups_workouts_out = (
#             await teams_groups_workouts_service.get_by_workout_id(
#                 workout_id=trainer_workout_out.workout_id
#             )
#         )
#         workout_schema: (
#             schemas.TrainerSportsmanWorkoutOut
#             | schemas.TrainerGroupWorkoutOut
#             | schemas.TrainerTeamWorkoutOut
#         )
#         if teams_groups_workouts_out:
#             team_id = teams_groups_workouts_out.team_id
#             group_id = teams_groups_workouts_out.group_id
#             if team_id:
#                 workout_schema = schemas.TrainerTeamWorkoutOut(
#                     **base_workouts_schemas.model_dump(),
#                     workout_type=consts.WorkoutsTypes.TEAM,
#                     team_id=team_id,
#                 )
#             elif group_id:
#                 workout_schema = schemas.TrainerGroupWorkoutOut(
#                     **base_workouts_schemas.model_dump(),
#                     workout_type=consts.WorkoutsTypes.GROUP,
#                     group_id=group_id,
#                 )
#             else:
#                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             await sportsmans_workouts_service.
