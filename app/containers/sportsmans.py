from dependency_injector import providers

from app.models import Sportsmans, SportsmansGroups
from app.repositories import SportsmansRepository
from app.services import SportsmansService

from .base_class import BaseContainer


class SportsmansContainer(BaseContainer):
    repository = providers.Factory(
        SportsmansRepository,
        model=Sportsmans,
        association_model=SportsmansGroups,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(SportsmansService, repository=repository)
