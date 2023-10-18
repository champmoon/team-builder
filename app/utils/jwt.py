import json
from datetime import datetime, timedelta

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from app.conf.settings import settings
from app.schemas import TokensDecodedSchema


class JWTManager:
    algorithm = settings.JWT_ALGORITHM

    secret_key = settings.JWT_SECRET_KEY
    secret_refresh_key = settings.JWT_REFRESH_SECRET_KEY

    access_token_expire = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire = settings.REFRESH_TOKEN_EXPIRE_MINUTES

    def create_token(
        self,
        data: TokensDecodedSchema,
        expire_time_minutes: float,
        secret_key: str,
        algorithm: str | None = None,
    ) -> str:
        if algorithm is None:
            algorithm = self.algorithm

        expire_time = datetime.utcnow() + timedelta(minutes=expire_time_minutes)

        to_encode = {"exp": expire_time, "sub": json.dumps(data.model_dump())}

        return str(jwt.encode(to_encode, secret_key, algorithm))

    def decode_token(
        self, token: str, secret_key: str, algorithm: str | None = None
    ) -> TokensDecodedSchema | None:
        if algorithm is None:
            algorithm = self.algorithm

        try:
            decoded_data = jwt.decode(token, secret_key, algorithm)["sub"]

            return TokensDecodedSchema(**json.loads(decoded_data))
        except (JWTError, JWTClaimsError, ExpiredSignatureError):
            return None

    def create_access_token(self, data: TokensDecodedSchema) -> str:
        return self.create_token(
            data=data,
            expire_time_minutes=self.access_token_expire,
            secret_key=self.secret_key,
        )

    def decode_access_token(self, token: str) -> TokensDecodedSchema | None:
        return self.decode_token(
            token=token,
            secret_key=self.secret_key,
        )
