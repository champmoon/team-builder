import datetime
from typing import Callable, Sequence
from uuid import UUID

from pydantic import NaiveDatetime

from app import schemas
from app.cache import actions as acts
from app.models import HealthQuestionnaires
from app.repositories import HealthQuestionnairesRepository


class HealthQuestinnairesService:
    def __init__(
        self,
        repository: HealthQuestionnairesRepository,
        health_questionnaire_action_part: Callable[
            [str, str | None], acts.Actions.health_questionnaire
        ],
    ) -> None:
        self.repository = repository
        self.health_questionnaire_action_part = health_questionnaire_action_part

    async def get_active(self, sportsman_id: UUID) -> HealthQuestionnaires | None:
        health_questionnaire_action = self.health_questionnaire_action_part(
            sportsman_id=str(sportsman_id)  # type: ignore
        )
        active_health_qs_id = await health_questionnaire_action.get_health_qs()  # noqa
        if active_health_qs_id is None:
            return None

        return await self.repository.get_by_id(id=UUID(active_health_qs_id))

    async def get_by_id(self, id: UUID) -> HealthQuestionnaires | None:
        return await self.repository.get_by_id(id=id)

    async def get_by_sportsman_id(
        self,
        sportsman_id: UUID,
        start_date: NaiveDatetime | None = None,
        end_date: NaiveDatetime | None = None,
    ) -> Sequence[HealthQuestionnaires]:
        health_questionnaire_action = self.health_questionnaire_action_part(
            sportsman_id=str(sportsman_id)  # type: ignore
        )
        active_health_qs_id = await health_questionnaire_action.get_health_qs()  # noqa
        active_health_qs_uuid: UUID | None
        if isinstance(active_health_qs_id, str):
            active_health_qs_uuid = UUID(active_health_qs_id)
        else:
            active_health_qs_uuid = active_health_qs_id

        return await self.repository.get_by_sportsman_id(
            sportsman_id=sportsman_id,
            exclude_today_id=active_health_qs_uuid,
            start_date=start_date,
            end_date=end_date,
        )

    async def create(
        self,
        schema_in: schemas.CreateHealthQuestionnaireIn,
    ) -> HealthQuestionnaires:
        new_health_questionnaire_out = await self.repository.create(schema_in=schema_in)

        today = datetime.datetime.now()
        next_day = today + datetime.timedelta(days=1)
        formatted_day = next_day.replace(hour=0, minute=0, second=1, microsecond=0)
        exp_time = round((formatted_day - today).total_seconds())

        health_questionnaire_action = self.health_questionnaire_action_part(
            sportsman_id=str(schema_in.sportsman_id),  # type: ignore
            health_questionnaire_id=str(new_health_questionnaire_out.id),
        )
        await health_questionnaire_action.set_full(timeout=exp_time)

        return new_health_questionnaire_out

    async def set_on_next_day(
        self,
        sportsman_id: UUID,
    ) -> None:
        today = datetime.datetime.now()
        next_day = today + datetime.timedelta(days=1)
        formatted_day = next_day.replace(hour=0, minute=0, second=1, microsecond=0)
        exp_time = round((formatted_day - today).total_seconds())

        health_questionnaire_action = self.health_questionnaire_action_part(
            sportsman_id=str(sportsman_id)  # type: ignore
        )
        await health_questionnaire_action.set_pre(timeout=exp_time)

    async def update(
        self,
        id: UUID,
        sportsman_id: UUID,
        schema_in: schemas.UpdateHealthQuestionnaireIn,
    ) -> HealthQuestionnaires | None:
        health_questionnaire_action = self.health_questionnaire_action_part(
            sportsman_id=str(sportsman_id),  # type: ignore
            health_questionnaire_id=str(id),
        )
        if not await health_questionnaire_action.is_set_full():
            return None

        await health_questionnaire_action.rmv_full()

        return await self.repository.update(id=id, schema_in=schema_in)
