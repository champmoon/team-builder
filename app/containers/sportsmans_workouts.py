from dependency_injector import providers

from app.cache.actions import Actions, create_action
from app.models import SportsmansWorkouts, WorkoutsStatuses
from app.repositories import SportsmansWorkoutsRepository, WorkoutsStatusesRepository
from app.services import SportsmansWorkoutsService

from .base_class import BaseContainer


class SportsmansWorkoutsContainer(BaseContainer):
    repository = providers.Factory(
        SportsmansWorkoutsRepository,
        model=SportsmansWorkouts,
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
        SportsmansWorkoutsService,
        repository=repository,
        statuses_repository=statuses_repository,
        workouts_status_action_part=workouts_status_action_part,
    )
