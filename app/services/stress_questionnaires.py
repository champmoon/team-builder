from typing import Callable
from uuid import UUID

from app.cache import actions as acts
from app.models import StressQuestionnaires
from app.repositories import StressQuestionnairesRepository


class StressQuestinnairesService:
    def __init__(
        self,
        repository: StressQuestionnairesRepository,
        stress_questionnaire_action_part: Callable[
            [str, str | None], acts.Actions.stress_questionnaire
        ],
    ) -> None:
        self.repository = repository
        self.stress_questionnaire_action_part = stress_questionnaire_action_part

    async def get_active_stress_questionnaires(
        self, sportsman_id: UUID
    ) -> list[StressQuestionnaires]:
        stress_questionnaire_action = self.stress_questionnaire_action_part(
            sportsman_id=str(sportsman_id)
        )
        active_stress_qs = await stress_questionnaire_action.get_all_stress_qs()

        return await self.repository.get_by_ids(ids=active_stress_qs)
