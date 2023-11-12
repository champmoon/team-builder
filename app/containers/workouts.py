from dependency_injector import providers

from app import models
from app.repositories import Repositories
from app.services import Services

from .base_class import BaseContainer


class WorkoutContainer(BaseContainer):
    repository = providers.Factory(
        Repositories.workouts,
        model=models.Workouts,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(
        Services.workouts,
        repository=repository,
        exercises_service=providers.Factory(
            Services.exercises,
            repository=providers.Factory(
                Repositories.exercises,
                model=models.Exercises,
                session_factory=BaseContainer.session_factory.provided.session,
            ),
            exercises_types_service=providers.Factory(
                Services.exercises_types,
                repository=providers.Factory(
                    Repositories.exercises_types,
                    model=models.ExercisesTypes,
                    session_factory=BaseContainer.session_factory.provided.session,
                )
            )
        ),
        sportsmans_workouts_service=providers.Factory(
            Services.sportsmans_workouts,
            repository=providers.Factory(
                Repositories.sportsmans_workouts,
                model=models.SportsmansWorkouts,
                session_factory=BaseContainer.session_factory.provided.session,
            )
        ),
        trainers_workouts_service=providers.Factory(
            Services.trainers_workouts,
            repository=providers.Factory(
                Repositories.trainers_workouts,
                model=models.TrainersWorkouts,
                session_factory=BaseContainer.session_factory.provided.session,
            )
        ),
        workouts_statuses_service=providers.Factory(
            Services.workouts_statuses,
            repository=providers.Factory(
                Repositories.workouts_statuses,
                model=models.WorkoutsStatuses,
                session_factory=BaseContainer.session_factory.provided.session,
            )
        ),
        exercises_types_service=providers.Factory(
            Services.exercises_types,
            repository=providers.Factory(
                Repositories.exercises_types,
                model=models.ExercisesTypes,
                session_factory=BaseContainer.session_factory.provided.session,
            )
        )
    )
