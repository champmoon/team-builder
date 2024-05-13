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
    response_model=schemas.ExercisesTypesOut,
    status_code=status.HTTP_201_CREATED,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def create_exercise_type(
    create_type_in: schemas.CreateExercisesTypeIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    exercises_types_service: Services.exercises_types = Depends(
        Provide[Containers.exercises_types.service],
    ),
) -> Any:
    exercise_type_out = await exercises_types_service.get_by_type(
        type=create_type_in.type, trainer_id=self_trainer.id
    )
    if exercise_type_out:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="exercises_type"
        )

    return await exercises_types_service.create(
        trainer_id=self_trainer.id, schema_in=create_type_in
    )


@router(
    response_model=schemas.ExercisesTypesOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def update_exercise_type(
    update_type_in: schemas.UpdateExercisesTypeIn,
    self_trainer: Trainers = Depends(deps.self_trainer),
    exercises_types_service: Services.exercises_types = Depends(
        Provide[Containers.exercises_types.service],
    ),
) -> Any:
    exercise_type_out = await exercises_types_service.get_by_type(
        type=update_type_in.type, trainer_id=self_trainer.id
    )
    if not exercise_type_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="exercises_type"
        )

    return await exercises_types_service.update(
        trainer_id=self_trainer.id, schema_in=update_type_in
    )


@router(
    response_model=schemas.ExercisesTypesOut,
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def delete_exercise_type(
    type: int,
    self_trainer: Trainers = Depends(deps.self_trainer),
    exercises_types_service: Services.exercises_types = Depends(
        Provide[Containers.exercises_types.service],
    ),
) -> Any:
    exercise_type_out = await exercises_types_service.get_by_type(
        type=type, trainer_id=self_trainer.id
    )
    if not exercise_type_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="exercises_type"
        )

    return await exercises_types_service.delete(type=type, trainer_id=self_trainer.id)


@router(
    response_model=list[schemas.ExercisesTypesOut],
    status_code=status.HTTP_200_OK,
)
@deps.auth_required(users=[UsersTypes.TRAINER])
@inject
async def reset_exercises_types(
    self_trainer: Trainers = Depends(deps.self_trainer),
    exercises_types_service: Services.exercises_types = Depends(
        Provide[Containers.exercises_types.service],
    ),
) -> Any:
    await exercises_types_service.delete_by_trainer_id(trainer_id=self_trainer.id)
    await exercises_types_service.initialize_defaults(trainer_id=self_trainer.id)

    return await exercises_types_service.get_all(trainer_id=self_trainer.id)
