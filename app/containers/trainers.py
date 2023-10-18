from dependency_injector import providers

from app.models import Trainers
from app.repositories import TrainersRepository
from app.services import TrainersService

from .base_class import BaseContainer


class TrainersContainer(BaseContainer):
    repository = providers.Factory(
        TrainersRepository,
        model=Trainers,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(TrainersService, repository=repository)
