from uuid import UUID

from .base_class import ActionTypes, BaseAction, BaseActionData


class InviteData(BaseActionData):
    team_id: UUID
    fake_id: UUID | None = None


class InviteAction(BaseAction[InviteData]):
    timeout = 300

    action_type = ActionTypes.INVITE
    action_data = InviteData
