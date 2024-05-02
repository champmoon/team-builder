from uuid import UUID

from .health_questionnaires import create_health_questionnaire


async def dispath_tasks(key: str) -> None:
    match key.split("_"):
        case "pre", "health", "questionnaire", sportsman_id:
            await create_health_questionnaire(sportsman_id=UUID(sportsman_id))
