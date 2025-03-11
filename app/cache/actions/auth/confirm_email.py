from .base_class import ActionTypes, BaseAction, BaseActionData

# class ConfirmTrainerEmailData(BaseActionData):
#     email: str
#     # first_name: str | None = None
#     # middle_name: str | None = None
#     # last_name: str | None = None
#     # team_name: str
#     # sport_type: SportsTypes


# class ConfirmTrainerEmailAction(BaseAction[ConfirmTrainerEmailData]):
#     timeout = 300

#     action_type = ActionTypes.CONFIRM_TRAINER_EMAIL
#     action_data = ConfirmTrainerEmailData


# class ConfirmSportsmanEmailData(BaseActionData):
#     email: str
#     # sport_type: SportsTypes
#     trainer_id: UUID


# class ConfirmSportsmanEmailAction(BaseAction[ConfirmSportsmanEmailData]):
#     timeout = 300

#     action_type = ActionTypes.CONFIRM_SPORTSMAN_EMAIL
#     action_data = ConfirmSportsmanEmailData


class ConfirmEmailData(BaseActionData):
    email: str
    # sport_type: SportsTypes
    is_trainer: bool


class ConfirmEmailAction(BaseAction[ConfirmEmailData]):
    timeout = 300

    action_type = ActionTypes.CONFIRM_EMAIL
    action_data = ConfirmEmailData


class GetConfirmEmailAction(BaseAction[ConfirmEmailData]):
    timeout = 300

    action_type = ActionTypes.GET_CONFIRM_EMAIL
    action_data = ConfirmEmailData
