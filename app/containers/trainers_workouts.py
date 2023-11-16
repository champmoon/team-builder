from dependency_injector import providers

from app.models import TrainersWorkouts
from app.repositories import TrainersWorkoutsRepository
from app.services import TrainersWorkoutsService

from .base_class import BaseContainer


class TrainersWorkoutsContainer(BaseContainer):
    repository = providers.Factory(
        TrainersWorkoutsRepository,
        model=TrainersWorkouts,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(TrainersWorkoutsService, repository=repository)
