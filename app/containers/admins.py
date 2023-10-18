from dependency_injector import providers

from app.models import Admins
from app.repositories import AdminsRepository
from app.services import AdminsService

from .base_class import BaseContainer


class AdminsContainer(BaseContainer):
    repository = providers.Factory(
        AdminsRepository,
        model=Admins,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(AdminsService, repository=repository)
