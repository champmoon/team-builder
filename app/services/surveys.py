from uuid import UUID

from app import schemas
from app.models import TeamSurveys
from app.repositories import TeamSurveysRepository

from app import consts


class TeamSurveysService:
    def __init__(self, repository: TeamSurveysRepository) -> None:
        self.repository = repository

    async def get_all(self) -> TeamSurveys | None:
        return await self.repository.get_all()

    async def create(
        self,
        team_id: UUID,
        sport_type: consts.SportsTypes,
    ) -> TeamSurveys:
        return await self.repository.create(
            team_id=team_id,
            main_fields=consts.SURVEY_SPORTS_MAIN_DATA[sport_type],
        )
