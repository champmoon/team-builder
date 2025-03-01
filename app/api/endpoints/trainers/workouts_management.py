from typing import Any
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from app import consts, schemas
from app.api import deps
from app.consts import UsersTypes, WorkoutsStatusesEnum
from app.containers import Containers
from app.models import Trainers, TrainersWorkouts, Workouts
from app.services import Services
from app.utils.router import EndPointRouter

router = EndPointRouter()


@inject
async def get_workout_schema(
    workout_out: Workouts,
    trainer_workout_out: TrainersWorkouts,
    tgs_workouts_service: Services.tgs_workouts = Depends(
        Provide[Containers.tgs_workouts.service]
    ),
) -> (
    schemas.TrainerSportsmanWorkoutOut
    | schemas.TrainerGroupWorkoutOut
    | schemas.TrainerTeamWorkoutOut
):
    base_workouts_schemas = schemas.TrainerWorkoutOut(
        id=workout_out.id,
        name=workout_out.workout_pool.name,
        estimated_time=workout_out.workout_pool.estimated_time,
        status=schemas.WorkoutsStatusesOut(
            status=consts.WorkoutsStatusesEnum(trainer_workout_out.status.status),
            description=consts.WORKOUTS_STATUSES_DESC[
                consts.WorkoutsStatusesEnum(trainer_workout_out.status.status)
            ],
        ),
        date=workout_out.date,
        created_at=workout_out.workout_pool.created_at,
        exercises=workout_out.workout_pool.exercises,
        rest_time=workout_out.rest_time,
        stress_questionnaire_time=workout_out.stress_questionnaire_time,
        comment=workout_out.comment,
        goal=workout_out.goal,
        repeat_id=workout_out.repeat_id,
    )

    tgs_workouts_out = await tgs_workouts_service.get_by_workout_id(
        workout_id=trainer_workout_out.workout_id
    )
    if not tgs_workouts_out:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_workout not found in tgs",
        )

    workout_schema: (
        schemas.TrainerSportsmanWorkoutOut
        | schemas.TrainerGroupWorkoutOut
        | schemas.TrainerTeamWorkoutOut
    )
    team_id = tgs_workouts_out.team_id
    group_id = tgs_workouts_out.group_id
    sportsman_id = tgs_workouts_out.sportsman_id
    if team_id:
        workout_schema = schemas.TrainerTeamWorkoutOut(
            **base_workouts_schemas.model_dump(),
            team_id=team_id,
        )
    elif group_id:
        workout_schema = schemas.TrainerGroupWorkoutOut(
            **base_workouts_schemas.model_dump(),
            group_id=group_id,
        )
    elif sportsman_id:
        workout_schema = schemas.TrainerSportsmanWorkoutOut(
            **base_workouts_schemas.model_dump(),
            sportsman_id=sportsman_id,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="_tgs all none ids",
        )

    return workout_schema


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def start_workout(
    id: UUID,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(Provide[Containers.workouts.service]),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out or workout_out.workout_pool.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    trainer_workout_out = await trainers_workouts_service.get_by(
        workout_id=workout_out.id,
        trainer_id=self_trainer.id,
    )
    if not trainer_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    if WorkoutsStatusesEnum(trainer_workout_out.status.status) not in (
        WorkoutsStatusesEnum.PLANNED,
        WorkoutsStatusesEnum.IN_PROGRESS,
        WorkoutsStatusesEnum.ACTIVE,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="workout_status",
        )

    await workouts_service.start(workout_id=workout_out.id)
    trainer_workout_out = await trainers_workouts_service.in_progress(
        schema_in=schemas.UpdateTrainerWorkoutIn(
            trainer_id=self_trainer.id,
            workout_id=workout_out.id,
        )
    )
    all_sportsmans_workouts_out = (
        await sportsmans_workouts_service.get_all_by_workout_id(workout_id=id)
    )
    for sportsman_workout_out in all_sportsmans_workouts_out:
        if WorkoutsStatusesEnum(sportsman_workout_out.status.status) not in (
            WorkoutsStatusesEnum.PLANNED,
            WorkoutsStatusesEnum.ACTIVE,
        ):
            continue

        await sportsmans_workouts_service.in_progress(
            schema_in=schemas.UpdateSportsmansWorkoutIn(
                sportsman_id=sportsman_workout_out.sportsman_id,
                workout_id=workout_out.id,
            )
        )

    return await get_workout_schema(
        workout_out=workout_out, trainer_workout_out=trainer_workout_out
    )


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def start_workout_for_sportsmans(
    id: UUID,
    sportsmans_emails_in: schemas.ListSportsmansEmailsIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service]
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out or workout_out.workout_pool.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    trainer_workout_out = await trainers_workouts_service.get_by(
        workout_id=workout_out.id,
        trainer_id=self_trainer.id,
    )
    if not trainer_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    if WorkoutsStatusesEnum(trainer_workout_out.status.status) not in (
        WorkoutsStatusesEnum.PLANNED,
        WorkoutsStatusesEnum.IN_PROGRESS,
        WorkoutsStatusesEnum.ACTIVE,
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="workout_status",
        )

    in_progress_sportsmans_cnt = 0
    sportsmans_emails = set(sportsmans_emails_in.sportsmans_emails)
    other_sportsmans_id: list[UUID] = []
    all_sportsmans_workouts_out = (
        await sportsmans_workouts_service.get_all_by_workout_id(workout_id=id)
    )
    for sportsman_workout_out in all_sportsmans_workouts_out:
        sportsman_out = await sportsmans_service.get_by_id(
            id=sportsman_workout_out.sportsman_id
        )
        if not sportsman_out:
            continue

        is_status = WorkoutsStatusesEnum(sportsman_workout_out.status.status) in (
            WorkoutsStatusesEnum.PLANNED,
            WorkoutsStatusesEnum.ACTIVE,
        )
        is_known = sportsman_out.email in sportsmans_emails
        if is_status and is_known:
            await sportsmans_workouts_service.in_progress(
                schema_in=schemas.UpdateSportsmansWorkoutIn(
                    sportsman_id=sportsman_workout_out.sportsman_id,
                    workout_id=workout_out.id,
                )
            )
            in_progress_sportsmans_cnt += 1
        elif is_status:
            other_sportsmans_id.append(sportsman_workout_out.sportsman_id)

    if in_progress_sportsmans_cnt == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="sportsmans"
        )

    await workouts_service.start(workout_id=workout_out.id)
    for sportsman_id in other_sportsmans_id:
        await sportsmans_workouts_service.active(
            schema_in=schemas.UpdateSportsmansWorkoutIn(
                sportsman_id=sportsman_id,
                workout_id=workout_out.id,
            )
        )

    trainer_workout_out = await trainers_workouts_service.in_progress(
        schema_in=schemas.UpdateTrainerWorkoutIn(
            trainer_id=self_trainer.id,
            workout_id=workout_out.id,
        )
    )

    return await get_workout_schema(
        workout_out=workout_out, trainer_workout_out=trainer_workout_out
    )


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def complete_workout(
    id: UUID,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
    health_questionnaires_service: Services.health_questionnaires = Depends(
        Provide[Containers.health_questionnaires.service],
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out or workout_out.workout_pool.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    trainer_workout_out = await trainers_workouts_service.get_by(
        workout_id=workout_out.id,
        trainer_id=self_trainer.id,
    )
    if not trainer_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    if (
        WorkoutsStatusesEnum(trainer_workout_out.status.status)
        != WorkoutsStatusesEnum.IN_PROGRESS
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="workout_status",
        )

    trainer_workout_out = await trainers_workouts_service.completed(
        schema_in=schemas.UpdateTrainerWorkoutIn(
            trainer_id=self_trainer.id,
            workout_id=workout_out.id,
        )
    )
    all_sportsmans_workouts_out = (
        await sportsmans_workouts_service.get_all_by_workout_id(workout_id=id)
    )
    for sportsman_workout_out in all_sportsmans_workouts_out:
        if (
            WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            != WorkoutsStatusesEnum.IN_PROGRESS
        ):
            continue

        await sportsmans_workouts_service.completed(
            schema_in=schemas.UpdateSportsmansWorkoutIn(
                sportsman_id=sportsman_workout_out.sportsman_id,
                workout_id=workout_out.id,
            )
        )

        await stress_questionnaires_service.create(
            schema_in=schemas.CreateStressQuestionnaireIn(
                sportsman_id=sportsman_workout_out.sportsman_id,
                workout_id=workout_out.id,
            ),
            timeout=workout_out.stress_questionnaire_time,
        )

        await health_questionnaires_service.set_on_next_day(
            sportsman_id=sportsman_workout_out.sportsman_id
        )

    return await get_workout_schema(
        workout_out=workout_out, trainer_workout_out=trainer_workout_out
    )


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def complete_workout_for_sportsmans(
    id: UUID,
    sportsmans_emails_in: schemas.ListSportsmansEmailsIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service]
    ),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
    health_questionnaires_service: Services.health_questionnaires = Depends(
        Provide[Containers.health_questionnaires.service],
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out or workout_out.workout_pool.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    trainer_workout_out = await trainers_workouts_service.get_by(
        workout_id=workout_out.id,
        trainer_id=self_trainer.id,
    )
    if not trainer_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    if (
        WorkoutsStatusesEnum(trainer_workout_out.status.status)
        != WorkoutsStatusesEnum.IN_PROGRESS
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="workout_status",
        )

    completed_sportsmans_cnt = 0
    other_completed_sportsmans_cnt = 0
    canceled_sportsmans_cnt = 0
    sportsmans_emails = set(sportsmans_emails_in.sportsmans_emails)
    all_sportsmans_workouts_out = (
        await sportsmans_workouts_service.get_all_by_workout_id(workout_id=id)
    )
    for sportsman_workout_out in all_sportsmans_workouts_out:
        sportsman_out = await sportsmans_service.get_by_id(
            id=sportsman_workout_out.sportsman_id
        )
        if not sportsman_out:
            continue

        is_status = (
            WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            == WorkoutsStatusesEnum.IN_PROGRESS
        )
        is_known = sportsman_out.email in sportsmans_emails
        if is_status and is_known:
            await sportsmans_workouts_service.completed(
                schema_in=schemas.UpdateSportsmansWorkoutIn(
                    sportsman_id=sportsman_out.id,
                    workout_id=workout_out.id,
                )
            )
            completed_sportsmans_cnt += 1

            await stress_questionnaires_service.create(
                schema_in=schemas.CreateStressQuestionnaireIn(
                    sportsman_id=sportsman_out.id,
                    workout_id=workout_out.id,
                ),
                timeout=workout_out.stress_questionnaire_time,
            )

            await health_questionnaires_service.set_on_next_day(
                sportsman_id=sportsman_out.id
            )

        if (
            WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            == WorkoutsStatusesEnum.COMPLETED
        ):
            other_completed_sportsmans_cnt += 1

        if (
            WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            == WorkoutsStatusesEnum.CANCELED
        ):
            canceled_sportsmans_cnt += 1

    if completed_sportsmans_cnt == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="sportsmans"
        )

    if (
        completed_sportsmans_cnt
        + other_completed_sportsmans_cnt
        + canceled_sportsmans_cnt
        == len(all_sportsmans_workouts_out)
    ):
        trainer_workout_out = await trainers_workouts_service.completed(
            schema_in=schemas.UpdateTrainerWorkoutIn(
                trainer_id=self_trainer.id,
                workout_id=workout_out.id,
            )
        )

    return await get_workout_schema(
        workout_out=workout_out, trainer_workout_out=trainer_workout_out
    )


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def cancel_workout(
    id: UUID,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
    health_questionnaires_service: Services.health_questionnaires = Depends(
        Provide[Containers.health_questionnaires.service],
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out or workout_out.workout_pool.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    trainer_workout_out = await trainers_workouts_service.get_by(
        workout_id=workout_out.id,
        trainer_id=self_trainer.id,
    )
    if not trainer_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    if (
        WorkoutsStatusesEnum(trainer_workout_out.status.status)
        != WorkoutsStatusesEnum.IN_PROGRESS
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="workout_status",
        )

    trainer_workout_out = await trainers_workouts_service.canceled(
        schema_in=schemas.UpdateTrainerWorkoutIn(
            trainer_id=self_trainer.id,
            workout_id=workout_out.id,
        )
    )
    all_sportsmans_workouts_out = (
        await sportsmans_workouts_service.get_all_by_workout_id(workout_id=id)
    )
    for sportsman_workout_out in all_sportsmans_workouts_out:
        if (
            WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            != WorkoutsStatusesEnum.IN_PROGRESS
        ):
            continue

        await sportsmans_workouts_service.canceled(
            schema_in=schemas.UpdateSportsmansWorkoutIn(
                sportsman_id=sportsman_workout_out.sportsman_id,
                workout_id=workout_out.id,
            )
        )

        await stress_questionnaires_service.create(
            schema_in=schemas.CreateStressQuestionnaireIn(
                sportsman_id=sportsman_workout_out.sportsman_id,
                workout_id=workout_out.id,
            ),
            timeout=workout_out.stress_questionnaire_time,
        )

        await health_questionnaires_service.set_on_next_day(
            sportsman_id=sportsman_workout_out.sportsman_id
        )

    return await get_workout_schema(
        workout_out=workout_out, trainer_workout_out=trainer_workout_out
    )


@router(
    response_model=schemas.TrainerWorkoutOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def cancel_workout_for_sportsmans(
    id: UUID,
    sportsmans_emails_in: schemas.ListSportsmansEmailsIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service]
    ),
    stress_questionnaires_service: Services.stress_questionnaires = Depends(
        Provide[Containers.stress_questionnaires.service],
    ),
    health_questionnaires_service: Services.health_questionnaires = Depends(
        Provide[Containers.health_questionnaires.service],
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out or workout_out.workout_pool.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    trainer_workout_out = await trainers_workouts_service.get_by(
        workout_id=workout_out.id,
        trainer_id=self_trainer.id,
    )
    if not trainer_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    if (
        WorkoutsStatusesEnum(trainer_workout_out.status.status)
        != WorkoutsStatusesEnum.IN_PROGRESS
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="workout_status",
        )

    completed_sportsmans_cnt = 0
    canceled_sportsmans_cnt = 0
    other_canceled_sportsmans_cnt = 0
    sportsmans_emails = set(sportsmans_emails_in.sportsmans_emails)
    all_sportsmans_workouts_out = (
        await sportsmans_workouts_service.get_all_by_workout_id(workout_id=id)
    )
    for sportsman_workout_out in all_sportsmans_workouts_out:
        sportsman_out = await sportsmans_service.get_by_id(
            id=sportsman_workout_out.sportsman_id
        )
        if not sportsman_out:
            continue

        is_status = (
            WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            == WorkoutsStatusesEnum.IN_PROGRESS
        )
        is_known = sportsman_out.email in sportsmans_emails
        if is_status and is_known:
            await sportsmans_workouts_service.canceled(
                schema_in=schemas.UpdateSportsmansWorkoutIn(
                    sportsman_id=sportsman_workout_out.sportsman_id,
                    workout_id=workout_out.id,
                )
            )
            canceled_sportsmans_cnt += 1

            await stress_questionnaires_service.create(
                schema_in=schemas.CreateStressQuestionnaireIn(
                    sportsman_id=sportsman_workout_out.sportsman_id,
                    workout_id=workout_out.id,
                ),
                timeout=workout_out.stress_questionnaire_time,
            )

            await health_questionnaires_service.set_on_next_day(
                sportsman_id=sportsman_workout_out.sportsman_id
            )

        if (
            WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            == WorkoutsStatusesEnum.CANCELED
        ):
            other_canceled_sportsmans_cnt += 1

        if (
            WorkoutsStatusesEnum(sportsman_workout_out.status.status)
            == WorkoutsStatusesEnum.COMPLETED
        ):
            completed_sportsmans_cnt += 1

    if canceled_sportsmans_cnt == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="sportsmans"
        )

    all_canceled_sportsmans_cnt = (
        other_canceled_sportsmans_cnt + canceled_sportsmans_cnt
    )
    if all_canceled_sportsmans_cnt == len(all_sportsmans_workouts_out):
        trainer_workout_out = await trainers_workouts_service.canceled(
            schema_in=schemas.UpdateTrainerWorkoutIn(
                trainer_id=self_trainer.id,
                workout_id=workout_out.id,
            )
        )
    elif completed_sportsmans_cnt + all_canceled_sportsmans_cnt == len(
        all_sportsmans_workouts_out
    ):
        trainer_workout_out = await trainers_workouts_service.completed(
            schema_in=schemas.UpdateTrainerWorkoutIn(
                trainer_id=self_trainer.id,
                workout_id=workout_out.id,
            )
        )

    return await get_workout_schema(
        workout_out=workout_out, trainer_workout_out=trainer_workout_out
    )


@router(
    response_model=list[schemas.SportsmanWithWorkoutStatusOut],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def get_workout_statuses(
    id: UUID,
    sportsmans_emails_in: schemas.ListSportsmansEmailsIn | None = None,
    self_trainer: Trainers = Depends(deps.self_trainer),
    workouts_service: Services.workouts = Depends(
        Provide[Containers.workouts.service],
    ),
    trainers_workouts_service: Services.trainers_workouts = Depends(
        Provide[Containers.trainers_workouts.service]
    ),
    sportsmans_workouts_service: Services.sportsmans_workouts = Depends(
        Provide[Containers.sportsmans_workouts.service]
    ),
    sportsmans_service: Services.sportsmans = Depends(
        Provide[Containers.sportsmans.service]
    ),
) -> Any:
    workout_out = await workouts_service.get_by_id(id=id)
    if not workout_out or workout_out.workout_pool.trainer_id != self_trainer.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    trainer_workout_out = await trainers_workouts_service.get_by(
        workout_id=workout_out.id,
        trainer_id=self_trainer.id,
    )
    if not trainer_workout_out:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workout")

    sportsmans_email_set = set(
        sportsmans_emails_in.sportsmans_emails if sportsmans_emails_in else []
    )
    response: list[schemas.SportsmanWithWorkoutStatusOut] = []
    sportsmans_workouts_out = await sportsmans_workouts_service.get_all_by_workout_id(
        workout_id=workout_out.id
    )
    for sportsman_workout_out in sportsmans_workouts_out:
        sportsman_out = await sportsmans_service.get_by_id(
            id=sportsman_workout_out.sportsman_id
        )
        if not sportsman_out:
            continue

        if (
            len(sportsmans_email_set) != 0
            and sportsman_out.email not in sportsmans_email_set
        ):
            continue

        response.append(
            schemas.SportsmanWithWorkoutStatusOut(
                sportsman_id=sportsman_out.id,
                workout_id=workout_out.id,
                email=sportsman_out.email,
                first_name=sportsman_out.first_name,
                middle_name=sportsman_out.middle_name,
                last_name=sportsman_out.last_name,
                status=schemas.WorkoutsStatusesOut(
                    status=consts.WorkoutsStatusesEnum(
                        sportsman_workout_out.status.status
                    ),
                    description=consts.WORKOUTS_STATUSES_DESC[
                        consts.WorkoutsStatusesEnum(sportsman_workout_out.status.status)
                    ],
                ),
            )
        )
    return response
