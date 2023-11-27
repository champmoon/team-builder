from dependency_injector import providers

from app.models import TGSWorkouts
from app.repositories import TGSWorkoutsRepository
from app.services import TGSWorkoutsService

from .base_class import BaseContainer


class TGSContainer(BaseContainer):
    repository = providers.Factory(
        TGSWorkoutsRepository,
        model=TGSWorkouts,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(TGSWorkoutsService, repository=repository)
