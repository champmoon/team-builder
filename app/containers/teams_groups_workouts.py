from dependency_injector import providers

from app.models import TeamsGroupsWorkouts
from app.repositories import TeamsGroupsWorkoutsRepository
from app.services import TeamsGroupsWorkoutsService

from .base_class import BaseContainer


class TeamsGroupsWorkoutsContainer(BaseContainer):
    repository = providers.Factory(
        TeamsGroupsWorkoutsRepository,
        model=TeamsGroupsWorkouts,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(TeamsGroupsWorkoutsService, repository=repository)
