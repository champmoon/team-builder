from uuid import UUID

from .base_class import ActionTypes, BaseAction, BaseActionData


class ResetEmailData(BaseActionData):
    email: str
    user_id: UUID


class ResetEmailAction(BaseAction[ResetEmailData]):
    timeout = 300

    action_type = ActionTypes.RESET_EMAIL
    action_data = ResetEmailData
