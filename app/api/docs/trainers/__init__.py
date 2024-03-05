from .auth import confirm_trainer_email, register_trainer, send_confirm_trainer_email
from .groups import (
    add_sportsman_to_group,
    adds_sportsmans_to_group,
    create_group,
    delete_group,
    get_self_group,
    get_self_groups,
    kick_sportsman_off_group,
    kicks_sportsmans_off_group,
    update_group,
)
from .profile import get_profile, update_profile, upload_avatar
from .teams import (
    add_sportsman_to_team,
    adds_sportsmans_to_team,
    get_self_team,
    kick_sportsman_off_team,
    kicks_sportsmans_off_team,
)
from .workouts import (
    create_workout_for_group,
    create_workout_for_sportsman,
    create_workout_for_team,
    delete_workout,
    get_workout,
    get_workouts,
    get_workouts_for_group,
    get_workouts_for_sportsman,
    get_workouts_for_team,
)
