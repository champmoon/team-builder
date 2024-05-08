from typing import TypeAlias

from .auth.check_confirm_email import CheckConfirmEmailAction, CheckConfirmEmailData
from .auth.confirm_email import (
    ConfirmSportsmanEmailAction,
    ConfirmSportsmanEmailData,
    ConfirmTrainerEmailAction,
    ConfirmTrainerEmailData,
)
from .auth.limit_email import LimitEmailAction, LimitEmailData
from .auth.limit_login import (
    LimitLoginAction,
    LimitLoginData,
    LoginLimitExceedException,
)
from .auth.reset_email import ResetEmailAction, ResetEmailData
from .auth.reset_password import ResetPasswordAction, ResetPasswordData
from .base import create_action
from .questionnaires.health import HealthQuestionnaireAction
from .questionnaires.stress import StressQuestionnaireAction
from .workouts.workout_status import WorkoutStatusAction


class Actions:
    limit_login: TypeAlias = LimitLoginAction
    check_confirm_email: TypeAlias = CheckConfirmEmailAction
    confirm_trainer_email: TypeAlias = ConfirmTrainerEmailAction
    confirm_sportsman_email: TypeAlias = ConfirmSportsmanEmailAction
    reset_email: TypeAlias = ResetEmailAction
    limit_email: TypeAlias = LimitEmailAction
    reset_password: TypeAlias = ResetPasswordAction

    stress_questionnaire: TypeAlias = StressQuestionnaireAction
    health_questionnaire: TypeAlias = HealthQuestionnaireAction

    workouts_status: TypeAlias = WorkoutStatusAction


class Data:
    limit_login: TypeAlias = LimitLoginData
    check_confirm_email: TypeAlias = CheckConfirmEmailData
    confirm_trainer_email: TypeAlias = ConfirmTrainerEmailData
    confirm_sportsman_email: TypeAlias = ConfirmSportsmanEmailData
    limit_email: TypeAlias = LimitEmailData
    reset_email: TypeAlias = ResetEmailData
    reset_password: TypeAlias = ResetPasswordData
