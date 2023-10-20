from dependency_injector import providers

from app.models import Groups
from app.repositories import GroupsRepository
from app.services import GroupsService

from .base_class import BaseContainer


class GroupsContainer(BaseContainer):
    repository = providers.Factory(
        GroupsRepository,
        model=Groups,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(GroupsService, repository=repository)
