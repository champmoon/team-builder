from dependency_injector import providers

from app.cache.actions import Actions, create_action
from app.models import Workouts, WorkoutsPool
from app.repositories import WorkoutsPoolRepository, WorkoutsRepository
from app.services import WorkoutsPoolService, WorkoutsService

from .base_class import BaseContainer


class WorkoutContainer(BaseContainer):
    repository = providers.Factory(
        WorkoutsRepository,
        model=Workouts,
        session_factory=BaseContainer.session_factory.provided.session,
    )

    workouts_status_action_part = providers.Callable(
        create_action,
        action_class=Actions.workouts_status,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )

    service = providers.Factory(
        WorkoutsService,
        repository=repository,
        workouts_status_action_part=workouts_status_action_part,
    )


class WorkoutPoolContainer(BaseContainer):
    repository = providers.Factory(
        WorkoutsPoolRepository,
        model=WorkoutsPool,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(WorkoutsPoolService, repository=repository)
