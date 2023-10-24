from dependency_injector import providers

from app.models import ExercisesTypes
from app.repositories import ExercisesTypesRepository
from app.services import ExercisesTypesService

from .base_class import BaseContainer


class ExercisesTypesContainer(BaseContainer):
    repository = providers.Factory(
        ExercisesTypesRepository,
        model=ExercisesTypes,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(ExercisesTypesService, repository=repository)
