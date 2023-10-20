from dependency_injector import providers

from app.models import Sportsmans
from app.repositories import SportsmansRepository
from app.services import SportsmansService

from .base_class import BaseContainer


class SportsmansContainer(BaseContainer):
    repository = providers.Factory(
        SportsmansRepository,
        model=Sportsmans,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(SportsmansService, repository=repository)
