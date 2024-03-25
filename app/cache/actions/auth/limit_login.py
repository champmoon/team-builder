from .base_class import ActionTypes, BaseAction, BaseActionData


class LoginLimitExceedException(Exception): ...


class LimitLoginData(BaseActionData):
    attempts: int


class LimitLoginAction(BaseAction[LimitLoginData]):
    max_attempts = 5

    timeout = 300

    action_type = ActionTypes.LIMIT_LOGIN
    action_data = LimitLoginData

    async def add_attempt(self) -> None:
        limit_login_data = await self.get()
        if not limit_login_data:
            return await self.set(self.action_data(attempts=1))

        if limit_login_data.attempts < self.max_attempts:
            return await self.set(
                self.action_data(attempts=limit_login_data.attempts + 1)
            )
        raise LoginLimitExceedException(
            f"Login attempts are more then {self.max_attempts}"
        )

    async def is_limited(self) -> bool:
        limit_login_data = await self.get()
        if limit_login_data:
            return limit_login_data.attempts == self.max_attempts
        return False
