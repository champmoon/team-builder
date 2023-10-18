import uuid
from functools import wraps
from inspect import Parameter, signature
from typing import Any, Callable

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

from app import consts, schemas
from app.containers import Containers
from app.models import Admins
from app.services import Services
from app.utils import JWTManager

get_bearer_token = HTTPBearer(auto_error=False)


async def get_authorization_data(
    auth: HTTPAuthorizationCredentials | None = Depends(get_bearer_token),
) -> schemas.TokensDecodedSchema:
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    jwt_manager = JWTManager()
    token_data = jwt_manager.decode_access_token(auth.credentials)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return token_data


def auth_required(*, users: list[consts.UsersTypes] | None = None) -> Callable:
    def auth(fastapi_endpoint: Callable) -> Callable:
        @wraps(fastapi_endpoint)
        async def wrapper(
            *args: Any,
            token_data: schemas.TokensDecodedSchema = Depends(get_authorization_data),
            **kwargs: Any,
        ) -> Any:
            if not users:
                return await fastapi_endpoint(*args, **kwargs)

            if token_data.user_type in users:
                return await fastapi_endpoint(*args, **kwargs)

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        params = list(signature(fastapi_endpoint).parameters.values())
        params.append(
            Parameter(
                "token_data",
                annotation=schemas.TokensDecodedSchema,
                kind=Parameter.KEYWORD_ONLY,
                default=Depends(get_authorization_data),
            )
        )
        setattr(
            fastapi_endpoint,
            "__signature__",
            signature(fastapi_endpoint).replace(parameters=tuple(params)),
        )

        return wrapper

    return auth


@inject
async def self_admin(
    token_data: schemas.TokensDecodedSchema = Depends(get_authorization_data),
    admin_service: Services.admins = Depends(Provide[Containers.admins.service]),
) -> Admins:
    admin_out = await admin_service.get_by_id(uuid.UUID(token_data.user_id))
    if not admin_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found"
        )
    return admin_out
