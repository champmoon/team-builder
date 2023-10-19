from dependency_injector import providers

from app.models import Teams
from app.repositories import TeamsRepository
from app.services import TeamsService

from .base_class import BaseContainer


class TeamsContainer(BaseContainer):
    repository = providers.Factory(
        TeamsRepository,
        model=Teams,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(TeamsService, repository=repository)
