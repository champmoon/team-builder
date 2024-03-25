from uuid import UUID

from .base_class import ActionTypes, BaseAction, BaseActionData


class ResetPasswordData(BaseActionData):
    user_id: UUID


class ResetPasswordAction(BaseAction[ResetPasswordData]):
    timeout = 300

    action_type = ActionTypes.RESET_PASSWORD
    action_data = ResetPasswordData
