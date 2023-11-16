from dependency_injector import providers

from app.models import Workouts
from app.repositories import WorkoutsRepository
from app.services import WorkoutsService

from .base_class import BaseContainer


class WorkoutContainer(BaseContainer):
    repository = providers.Factory(
        WorkoutsRepository,
        model=Workouts,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(WorkoutsService, repository=repository)
