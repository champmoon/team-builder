from uuid import UUID

from app import consts
from app.models import TeamSurveys
from app.repositories import TeamSurveysRepository


class TeamSurveysService:
    def __init__(self, repository: TeamSurveysRepository) -> None:
        self.repository = repository

    async def get_by_team_id(self, team_id: UUID) -> TeamSurveys | None:
        return await self.repository.get_by_team_id(team_id=team_id)

    async def create(
        self,
        team_id: UUID,
        sport_type: consts.SportsTypes,
    ) -> TeamSurveys:
        return await self.repository.create(
            team_id=team_id,
            main_fields=consts.TEAM_SURVEY_MAIN_DATA[sport_type],
            add_fields=consts.TEAM_SURVEY_ADD_DATA[sport_type],
        )

    async def update(self, id: UUID, add_fields: list) -> TeamSurveys:
        return await self.repository.update(id=id, add_fields=add_fields)
