from uuid import UUID

from app import consts
from app.models import SportsmanSurveys, TeamSurveys
from app.repositories import SportsmanSurveysRepository, TeamSurveysRepository


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


class SportsmanSurveysService:
    def __init__(self, repository: SportsmanSurveysRepository) -> None:
        self.repository = repository

    async def get_by_sportsman_id(self, sportsman_id: UUID) -> SportsmanSurveys | None:
        return await self.repository.get_by_sportsman_id(sportsman_id=sportsman_id)

    async def create(
        self,
        sportsman_id: UUID,
        team_survey_id: UUID,
    ) -> SportsmanSurveys:
        return await self.repository.create(
            sportsman_id=sportsman_id,
            team_survey_id=team_survey_id,
        )

    async def update(self, id: UUID, answers: list) -> SportsmanSurveys:
        return await self.repository.update(id=id, answers=answers)

    async def set_update(self, sportsman_id: UUID) -> SportsmanSurveys:
        return await self.repository.set_update(sportsman_id=sportsman_id)
