from dependency_injector import providers

from app.models import TeamSurveys
from app.repositories import TeamSurveysRepository
from app.services import TeamSurveysService

from .base_class import BaseContainer


class TeamSurveysContainer(BaseContainer):
    repository = providers.Factory(
        TeamSurveysRepository,
        model=TeamSurveys,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(TeamSurveysService, repository=repository)
