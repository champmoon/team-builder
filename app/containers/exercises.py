from dependency_injector import providers

from app.models import Exercises, ExercisesTypes
from app.repositories import ExercisesRepository, ExercisesTypesRepository
from app.services import ExercisesService, ExercisesTypesService

from .base_class import BaseContainer


class ExercisesContainer(BaseContainer):
    repository = providers.Factory(
        ExercisesRepository,
        model=Exercises,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(
        ExercisesService,
        repository=repository,
        exercises_types_service=providers.Factory(
            ExercisesTypesService,
            repository=providers.Factory(
                ExercisesTypesRepository,
                model=ExercisesTypes,
                session_factory=BaseContainer.session_factory.provided.session,
            ),
        ),
    )

