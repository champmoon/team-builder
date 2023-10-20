from dependency_injector import providers

from app.models import SportsmansGroups
from app.repositories import SportsmansGroupsRepository
from app.services import SportsmansGroupsService

from .base_class import BaseContainer


class SportsmansGroupsContainer(BaseContainer):
    repository = providers.Factory(
        SportsmansGroupsRepository,
        model=SportsmansGroups,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(SportsmansGroupsService, repository=repository)
