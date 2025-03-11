from dependency_injector import providers

from app.cache.actions import Actions, create_action
from app.services import AuthService

from .base_class import BaseContainer


class AuthContainer(BaseContainer):
    limit_login_action_part = providers.Callable(
        create_action,
        action_class=Actions.limit_login,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )

    confirm_email_action_part = providers.Callable(
        create_action,
        action_class=Actions.confirm_email,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )

    get_confirm_email_action_part = providers.Callable(
        create_action,
        action_class=Actions.get_confirm_email,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )

    check_confirm_email_action_part = providers.Callable(
        create_action,
        action_class=Actions.check_confirm_email,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )

    reset_email_action_part = providers.Callable(
        create_action,
        action_class=Actions.reset_email,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )

    reset_password_action_part = providers.Callable(
        create_action,
        action_class=Actions.reset_password,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )

    limit_email_action_part = providers.Callable(
        create_action,
        action_class=Actions.limit_email,
        connection_factory=BaseContainer.connection_factory.provided.connection,
    )

    service = providers.Factory(
        AuthService,
        limit_login_action_part=limit_login_action_part,
        confirm_email_action_part=confirm_email_action_part,
        get_confirm_email_action_part=get_confirm_email_action_part,
        check_confirm_email_action_part=check_confirm_email_action_part,
        limit_email_action_part=limit_email_action_part,
        reset_email_action_part=reset_email_action_part,
        reset_password_action_part=reset_password_action_part,
    )
