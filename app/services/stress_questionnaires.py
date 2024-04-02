from typing import Callable
from uuid import UUID

from app import schemas
from app.cache import actions as acts


class StressQuestinnairesService:
    def __init__(
        self,
        stress_questionnaire_action_part: Callable[
            [str, str | None], acts.Actions.stress_questionnaire
        ],
    ) -> None:
        self.stress_questionnaire_action_part = stress_questionnaire_action_part

    async def get_active_stress_questionnaires(
        self, sportsman_id: UUID
    ) -> list[schemas.GroupOut]:
        stress_questionnaire_action = self.stress_questionnaire_action_part(
            sportsman_id=str(sportsman_id)
        )
        await stress_questionnaire_action.get_all_stress_qs()
