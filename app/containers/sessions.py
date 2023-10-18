from dependency_injector import providers

from app.models import Sessions
from app.repositories import SessionsRepository
from app.services import SessionsService

from .base_class import BaseContainer


class SessionsContainer(BaseContainer):
    repository = providers.Factory(
        SessionsRepository,
        model=Sessions,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(SessionsService, repository=repository)
