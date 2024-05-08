from dependency_injector import providers

from app.cache.actions import Actions, create_action
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
    workouts_status_action_part = providers.Callable(
        create_action,
        action_class=Actions.workouts_status,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )
    service = providers.Factory(
        TrainersWorkoutsService,
        repository=repository,
        statuses_repository=statuses_repository,
        workouts_status_action_part=workouts_status_action_part,
    )
