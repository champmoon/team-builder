from .base_class import ActionTypes, BaseAction, BaseActionData


class CheckConfirmEmailData(BaseActionData):
    is_confirmed: bool


class CheckConfirmEmailAction(BaseAction[CheckConfirmEmailData]):
    timeout = 300

    action_type = ActionTypes.CHECK_CONFIRM_EMAIL
    action_data = CheckConfirmEmailData

    async def set_confirm_flag(self) -> None:
        check_confirm_email_data = await self.get()

        if not check_confirm_email_data:
            await self.set(self.action_data(is_confirmed=True))

    async def is_confirmed(self) -> bool:
        check_confirm_email_data = await self.get()
        return bool(check_confirm_email_data)
