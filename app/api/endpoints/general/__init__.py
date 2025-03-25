from .auth import (
    login,
    logout,
    refresh,
    verify,
)
from .exercises_types import get_exercises_types
from .password import confirm_password, reset_password, send_confirm_password
from .registration import confirm_email, register, send_confirm_email
from .workouts_statuses import get_workouts_statuses
