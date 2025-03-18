import logging
from typing import Callable
from uuid import UUID, uuid4

from app import schemas
from app.cache import actions as acts
from app.conf.settings import settings
from app.utils import Background, Hasher, JWTManager
from app.utils.email import Email

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(
        self,
        limit_login_action_part: Callable[[str], acts.Actions.limit_login],
        confirm_email_action_part: Callable[[str], acts.Actions.confirm_email],
        get_confirm_email_action_part: Callable[[str], acts.Actions.get_confirm_email],
        check_confirm_email_action_part: Callable[
            [str], acts.Actions.check_confirm_email
        ],
        limit_email_action_part: Callable[[str], acts.Actions.limit_email],
        reset_email_action_part: Callable[[str], acts.Actions.reset_email],
        reset_password_action_part: Callable[[str], acts.Actions.reset_password],
    ) -> None:
        self.limit_login_action_part = limit_login_action_part
        self.confirm_email_action_part = confirm_email_action_part
        self.get_confirm_email_action_part = get_confirm_email_action_part
        self.check_confirm_email_action_part = check_confirm_email_action_part
        self.limit_email_action_part = limit_email_action_part
        self.reset_email_action_part = reset_email_action_part
        self.reset_password_action_part = reset_password_action_part

    async def create_tokens(
        self,
        refresh_token: UUID,
        tokens_data: schemas.TokensEncodedSchema,
    ) -> schemas.TokensOut:
        return schemas.TokensOut(
            access_token=JWTManager().create_access_token(
                data=schemas.TokensDecodedSchema(
                    user_id=tokens_data.user_id,
                    user_type=tokens_data.user_type,
                )
            ),
            refresh_token=refresh_token,
            user_type=tokens_data.user_type,
        )

    async def is_match_passwords(
        self, login_password: str, hashed_password: str
    ) -> bool:
        return Hasher(secret=login_password).verify(hash=hashed_password)

    async def check_login_attempts(self, email: str) -> int | None:
        try:
            await self.limit_login_action_part(email).add_attempt()
        except acts.LoginLimitExceedException:
            return await self.limit_login_action_part(email).ttl()
        return None

    async def reset_login_attempts(self, email: str) -> None:
        await self.limit_login_action_part(email).rmv()

    async def is_limited(self, email: str) -> bool:
        return await self.limit_login_action_part(email).is_limited()

    async def get_limit_timer(self, email: str) -> int:
        return await self.limit_login_action_part(email).ttl()

    async def create_confirmation_url(self, confirm_data: schemas.SendEmailIn) -> str:
        confirm_token = uuid4()
        confirm_email_uri = (
            f"{settings.CONFIRM_URL}/register?confirm_token={confirm_token}"
        )

        confirm_email_action = self.confirm_email_action_part(str(confirm_token))
        await confirm_email_action.set(
            acts.ConfirmEmailData(
                email=confirm_data.email,
                user_type=confirm_data.user_type,
            )
        )
        return confirm_email_uri

    # async def create_trainer_confirmation_uri(
    #     self, confirm_data: schemas.SendTrainerEmailIn
    # ) -> str:
    #     confirm_token = uuid4()
    #     confirm_email_uri = (
    #         f"{settings.CONFIRM_URL}/register?confirm_token={confirm_token}"
    #     )

    #     confirm_email_action = self.confirm_trainer_email_action_part(
    #         str(confirm_token)
    #     )
    #     await confirm_email_action.set(
    #         acts.ConfirmTrainerEmailData(
    #             email=confirm_data.email,
    #             # first_name=confirm_data.first_name,
    #             # middle_name=confirm_data.middle_name,
    #             # last_name=confirm_data.last_name,
    #             # team_name=confirm_data.team_name,
    #             # sport_type=confirm_data.sport_type,
    #         )
    #     )
    #     return confirm_email_uri

    # async def create_sportsman_confirmation_uri(
    #     self, confirm_data: schemas.InnerSendSportsmanEmailIn
    # ) -> str:
    #     confirm_token = uuid4()
    #     confirm_email_uri = (
    #         f"{settings.CONFIRM_URL}/register?confirm_token={confirm_token}"
    #     )

    #     confirm_email_action = self.confirm_sportsman_email_action_part(
    #         str(confirm_token)
    #     )
    #     await confirm_email_action.set(
    #         acts.ConfirmSportsmanEmailData(
    #             email=confirm_data.email,
    #             # sport_type=confirm_data.sport_type,
    #             trainer_id=confirm_data.trainer_id,
    #         )
    #     )
    #     return confirm_email_uri

    # async def create_reset_email_uri(self, email: str, user_id: UUID) -> str:
    #     confirm_token = uuid4()
    #     change_email_uri = f"{settings.CONFIRM_URL}/reset?email={confirm_token}"

    #     reset_email_action = self.reset_email_action_part(str(confirm_token))
    #     await reset_email_action.set(
    # acts.ResetEmailData(email=email, user_id=user_id))

    #     return change_email_uri

    async def create_reset_password_uri(self, email: str) -> str:
        confirm_token = uuid4()
        reset_password_uri = (
            f"{settings.CONFIRM_URL}/reset-password?confirm_token={confirm_token}"
        )

        reset_password_action = self.reset_password_action_part(str(confirm_token))
        await reset_password_action.set(acts.ResetPasswordData(email=email))

        return reset_password_uri

    async def send_reset_password(self, email: str) -> None:
        reset_password_uri = await self.create_reset_password_uri(email=email)
        await self.send_email(to_email=email, confirm_email_uri=reset_password_uri)

    async def send_confirmation_email(self, confirm_data: schemas.SendEmailIn) -> None:
        confirm_email_uri = await self.create_confirmation_url(
            confirm_data=confirm_data
        )
        await self.send_email(
            to_email=confirm_data.email, confirm_email_uri=confirm_email_uri
        )

    # async def send_sportsman_confirmation_email(
    #     self, confirm_data: schemas.InnerSendSportsmanEmailIn
    # ) -> None:
    #     confirm_email_uri = await self.create_sportsman_confirmation_uri(
    #         confirm_data=confirm_data
    #     )
    #     await self.send_email(
    #         to_email=confirm_data.email, confirm_email_uri=confirm_email_uri
    #     )

    # async def send_reset_email(self, email: str, user_id: UUID) -> None:
    #     reset_email_uri = await self.create_reset_email_uri(
    #         email=email, user_id=user_id
    #     )
    #     await self.send_email(to_email=email, confirm_email_uri=reset_email_uri)

    # async def send_reset_password_email(self, email: str, user_id: UUID) -> None:
    #     reset_password_uri = await self.create_reset_password_uri(user_id=user_id)
    #     await self.send_email(to_email=email, confirm_email_uri=reset_password_uri)

    async def send_email(self, to_email: str, confirm_email_uri: str) -> None:
        try:
            coro = Email().send(to_email=to_email, uri=confirm_email_uri)
            Background().run(coro=coro)
        except ConnectionRefusedError as e:
            logger.warning(f"Email exception - {e}")

    async def get_data_by_confirm_token(
        self, confirm_token: str
    ) -> acts.ConfirmEmailData | None:
        confirm_email_action = self.confirm_email_action_part(confirm_token)
        confirm_email_data = await confirm_email_action.get()

        if not confirm_email_data:
            return None

        await confirm_email_action.rmv()

        get_confirm_email_action = self.get_confirm_email_action_part(
            confirm_email_data.email
        )
        await get_confirm_email_action.set(confirm_email_data)

        return confirm_email_data

    async def get_get_data_by_confirm_token(
        self, email: str
    ) -> acts.ConfirmEmailData | None:
        confirm_email_action = self.get_confirm_email_action_part(email)
        confirm_email_data = await confirm_email_action.get()

        if not confirm_email_data:
            return None

        await confirm_email_action.rmv()

        return confirm_email_data

    # async def get_sportsman_data_by_confirm_token(
    #     self, confirm_token: str
    # ) -> acts.ConfirmSportsmanEmailData | None:
    #     confirm_email_action = self.confirm_sportsman_email_action_part(confirm_token)
    #     confirm_email_data = await confirm_email_action.get()

    #     if not confirm_email_data:
    #         return None

    #     await confirm_email_action.rmv()

    #     return confirm_email_data

    async def get_reset_email_data_by_confirm_token(
        self, confirm_token: str
    ) -> acts.ResetEmailData | None:
        reset_email_action = self.reset_email_action_part(confirm_token)
        reset_email_data = await reset_email_action.get()

        if not reset_email_data:
            return None

        await reset_email_action.rmv()

        return reset_email_data

    async def get_reset_password_data_by_confirm_token(
        self, confirm_token: str
    ) -> acts.ResetPasswordData | None:
        reset_password_action = self.reset_password_action_part(confirm_token)
        reset_password_data = await reset_password_action.get()

        if not reset_password_data:
            return None

        await reset_password_action.rmv()

        return reset_password_data

    async def is_email_sended(self, email: str) -> bool:
        return await self.limit_email_action_part(email).is_blocked()

    async def get_email_block_timer(self, email: str) -> int:
        return await self.limit_email_action_part(email).ttl()

    async def set_email_sended(self, email: str) -> None:
        return await self.limit_email_action_part(email).set_send_flag()

    async def clear_limit_email(self, email: str) -> None:
        return await self.limit_email_action_part(email).rmv()

    async def is_email_confirmed(self, email: str) -> bool:
        return await self.check_confirm_email_action_part(email).is_confirmed()

    async def reset_email_confirm(self, email: str) -> None:
        return await self.check_confirm_email_action_part(email).reset()

    async def set_check_confirm_email(self, email: str) -> None:
        return await self.check_confirm_email_action_part(email).set_confirm_flag()
