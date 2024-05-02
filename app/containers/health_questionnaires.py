from dependency_injector import providers

from app.cache.actions import Actions, create_action
from app.models import HealthQuestionnaires
from app.repositories import HealthQuestionnairesRepository
from app.services import HealthQuestinnairesService

from .base_class import BaseContainer


class HealthQuestionnairesContainer(BaseContainer):
    repository = providers.Factory(
        HealthQuestionnairesRepository,
        model=HealthQuestionnaires,
        session_factory=BaseContainer.session_factory.provided.session,
    )

    health_questionnaire_action_part = providers.Callable(
        create_action,
        action_class=Actions.health_questionnaire,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )

    service = providers.Factory(
        HealthQuestinnairesService,
        repository=repository,
        health_questionnaire_action_part=health_questionnaire_action_part,
    )
