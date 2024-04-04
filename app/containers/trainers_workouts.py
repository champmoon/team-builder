from dependency_injector import providers

from app.models import TrainersWorkouts
from app.models.workouts_statuses import WorkoutsStatuses
from app.repositories import TrainersWorkoutsRepository
from app.repositories.workouts_statuses import WorkoutsStatusesRepository
from app.services import TrainersWorkoutsService

from .base_class import BaseContainer


class TrainersWorkoutsContainer(BaseContainer):
    repository = providers.Factory(
        TrainersWorkoutsRepository,
        model=TrainersWorkouts,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    statuses_repository = providers.Factory(
        WorkoutsStatusesRepository,
        model=WorkoutsStatuses,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(
        TrainersWorkoutsService,
        repository=repository,
        statuses_repository=statuses_repository,
    )
