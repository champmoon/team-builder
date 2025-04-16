from .base_class import ActionTypes, BaseAction, BaseActionData


class EmailAlreadySendedException(Exception): ...


class LimitEmailData(BaseActionData):
    send_flag: bool


class LimitEmailAction(BaseAction[LimitEmailData]):
    # timeout = 300
    timeout = 5

    action_type = ActionTypes.LIMIT_EMAIL
    action_data = LimitEmailData

    async def set_send_flag(self) -> None:
        limit_email_data = await self.get()

        if not limit_email_data:
            await self.set(self.action_data(send_flag=True))

    async def is_blocked(self) -> bool:
        limit_email_data = await self.get()
        return bool(limit_email_data)
