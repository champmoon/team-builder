from dependency_injector import providers

from app.services import AuthService

from .base_class import BaseContainer


class AuthContainer(BaseContainer):
    service = providers.Factory(AuthService)
