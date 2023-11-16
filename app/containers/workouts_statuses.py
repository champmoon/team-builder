from dependency_injector import providers

from app.models import WorkoutsStatuses
from app.repositories import WorkoutsStatusesRepository
from app.services import WorkoutsStatusesService

from .base_class import BaseContainer


class WorkoutsStatusesContainer(BaseContainer):
    repository = providers.Factory(
        WorkoutsStatusesRepository,
        model=WorkoutsStatuses,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(WorkoutsStatusesService, repository=repository)
