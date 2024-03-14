from dependency_injector import providers

from app.models import Workouts, WorkoutsPool
from app.repositories import WorkoutsRepository, WorkoutsPoolRepository
from app.services import WorkoutsService, WorkoutsPoolService

from .base_class import BaseContainer


class WorkoutContainer(BaseContainer):
    repository = providers.Factory(
        WorkoutsRepository,
        model=Workouts,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(WorkoutsService, repository=repository)


class WorkoutPoolContainer(BaseContainer):
    repository = providers.Factory(
        WorkoutsPoolRepository,
        model=WorkoutsPool,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(WorkoutsPoolService, repository=repository)
