from uuid import UUID

from app import schemas
from app.utils import Hasher, JWTManager


class AuthService:
    def __init__(self) -> None:
        pass

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
