from dependency_injector import providers

from app.cache.actions import Actions, create_action
from app.models import StressQuestionnaires
from app.repositories import StressQuestionnairesRepository
from app.services import StressQuestinnairesService

from .base_class import BaseContainer


class StressQuestionnairesContainer(BaseContainer):
    repository = providers.Factory(
        StressQuestionnairesRepository,
        model=StressQuestionnaires,
        session_factory=BaseContainer.session_factory.provided.session,
    )

    stress_questionnaire_action_part = providers.Callable(
        create_action,
        action_class=Actions.stress_questionnaire,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )

    service = providers.Factory(
        StressQuestinnairesService,
        repository=repository,
        stress_questionnaire_action_part=stress_questionnaire_action_part,
    )
