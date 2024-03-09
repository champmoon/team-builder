from dependency_injector import providers

from app.models import SportsmanSurveys, TeamSurveys
from app.repositories import SportsmanSurveysRepository, TeamSurveysRepository
from app.services import SportsmanSurveysService, TeamSurveysService

from .base_class import BaseContainer


class TeamSurveysContainer(BaseContainer):
    repository = providers.Factory(
        TeamSurveysRepository,
        model=TeamSurveys,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(TeamSurveysService, repository=repository)


class SportsmanSurveysContainer(BaseContainer):
    repository = providers.Factory(
        SportsmanSurveysRepository,
        model=SportsmanSurveys,
        session_factory=BaseContainer.session_factory.provided.session,
    )
    service = providers.Factory(SportsmanSurveysService, repository=repository)
