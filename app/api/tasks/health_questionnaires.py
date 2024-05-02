from uuid import UUID

from dependency_injector.wiring import Provide, inject

from app.containers import Containers
from app.schemas import CreateHealthQuestionnaireIn
from app.services import Services


@inject
async def create_health_questionnaire(
    sportsman_id: UUID,
    health_questionnaires_service: Services.health_questionnaires = Provide[
        Containers.health_questionnaires.service
    ],
) -> None:
    await health_questionnaires_service.create(
        CreateHealthQuestionnaireIn(sportsman_id=sportsman_id)
    )
