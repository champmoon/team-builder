from typing import TypeAlias

from .base_class import create_action
from .check_confirm_email import CheckConfirmEmailAction, CheckConfirmEmailData
from .confirm_email import (
    ConfirmSportsmanEmailAction,
    ConfirmSportsmanEmailData,
    ConfirmTrainerEmailAction,
    ConfirmTrainerEmailData,
)
from .limit_email import LimitEmailAction, LimitEmailData
from .limit_login import (
    LimitLoginAction,
    LimitLoginData,
    LoginLimitExceedException,
)
from .reset_email import ResetEmailAction, ResetEmailData
from .reset_password import ResetPasswordAction, ResetPasswordData


class Actions:
    limit_login: TypeAlias = LimitLoginAction
    check_confirm_email: TypeAlias = CheckConfirmEmailAction
    confirm_trainer_email: TypeAlias = ConfirmTrainerEmailAction
    confirm_sportsman_email: TypeAlias = ConfirmSportsmanEmailAction
    reset_email: TypeAlias = ResetEmailAction
    limit_email: TypeAlias = LimitEmailAction
    reset_password: TypeAlias = ResetPasswordAction


class Data:
    limit_login: TypeAlias = LimitLoginData
    check_confirm_email: TypeAlias = CheckConfirmEmailData
    confirm_trainer_email: TypeAlias = ConfirmTrainerEmailData
    confirm_sportsman_email: TypeAlias = ConfirmSportsmanEmailData
    limit_email: TypeAlias = LimitEmailData
    reset_email: TypeAlias = ResetEmailData
    reset_password: TypeAlias = ResetPasswordData
