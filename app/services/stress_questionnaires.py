from typing import Callable, Sequence
from uuid import UUID

from pydantic import NaiveDatetime

from app import schemas
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

    async def get_actives(self, sportsman_id: UUID) -> Sequence[StressQuestionnaires]:
        stress_questionnaire_action = self.stress_questionnaire_action_part(
            sportsman_id=str(sportsman_id)  # type: ignore
        )
        active_stress_qs_ids = [
            UUID(stress_questionnaire)
            for stress_questionnaire in await stress_questionnaire_action.get_all_stress_qs()  # noqa
        ]

        return await self.repository.get_by_ids(ids=active_stress_qs_ids)

    async def get_by_id(self, id: UUID) -> StressQuestionnaires | None:
        return await self.repository.get_by_id(id=id)

    async def get_by_workout_id(self, workout_id: UUID) -> StressQuestionnaires | None:
        return await self.repository.get_by_workout_id(workout_id=workout_id)

    async def get_all_by_sportsman_id(
        self,
        sportsman_id: UUID,
        start_date: NaiveDatetime | None = None,
        end_date: NaiveDatetime | None = None,
    ) -> Sequence[StressQuestionnaires]:
        return await self.repository.get_all_by_sportsman_id(
            sportsman_id=sportsman_id, start_date=start_date, end_date=end_date
        )

    async def get_all_by_workout_id(
        self, workout_id: UUID
    ) -> Sequence[StressQuestionnaires]:
        return await self.repository.get_all_by_workout_id(workout_id=workout_id)

    async def create(
        self,
        schema_in: schemas.CreateStressQuestionnaireIn,
        timeout: int,
    ) -> StressQuestionnaires:
        new_stress_questionnaire_out = await self.repository.create(schema_in=schema_in)

        stress_questionnaire_action = self.stress_questionnaire_action_part(
            sportsman_id=str(schema_in.sportsman_id),  # type: ignore
            stress_questionnaire_id=str(new_stress_questionnaire_out.id),
        )

        await stress_questionnaire_action.set(timeout=timeout)

        return new_stress_questionnaire_out

    async def update(
        self,
        id: UUID,
        sportsman_id: UUID,
        schema_in: schemas.UpdateStressQuestionnaireIn,
    ) -> StressQuestionnaires | None:
        stress_questionnaire_action = self.stress_questionnaire_action_part(
            sportsman_id=str(sportsman_id),  # type: ignore
            stress_questionnaire_id=str(id),
        )
        if not await stress_questionnaire_action.is_set():
            return None

        await stress_questionnaire_action.rmv()
        return await self.repository.update(id=id, schema_in=schema_in)
