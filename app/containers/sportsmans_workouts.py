from dependency_injector import providers

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
    service = providers.Factory(
        SportsmansWorkoutsService,
        repository=repository,
        statuses_repository=statuses_repository,
    )
