from .auth import confirm_trainer_email, register_trainer, send_confirm_trainer_email
from .exercises_types import (
    create_exercise_type,
    delete_exercise_type,
    reset_exercises_types,
    update_exercise_type,
)
from .groups import (
    add_sportsman_to_group,
    adds_sportsmans_to_group,
    create_group,
    delete_group,
    get_self_groups,
    kick_sportsman_off_group,
    kicks_sportsmans_off_group,
    update_group,
)
from .health_questionnaires import (
    get_all_health_questionnaires_by_sportsman,
    get_health_questionnaire,
)
from .profile import get_profile, update_profile, upload_avatar
from .stress_questionnaires import (
    get_all_stress_questionnaires_by_sportsman,
    get_all_stress_questionnaires_by_workout,
    get_stress_questionnaire,
)
from .surveys import (
    fill_survey_for_sportsman,
    get_sportsman_survey,
    get_survey,
    set_update_sportsman_survey,
    set_update_team_survey,
    update_survey,
)
from .teams import get_self_team
from .workouts import (
    create_workout_for_group,
    create_workout_for_sportsman,
    create_workout_for_team,
    delete_workout,
    get_workout,
    get_workouts,
    get_workouts_by_pool_id,
    get_workouts_for_group,
    get_workouts_for_sportsman,
    get_workouts_for_team,
    update_workout,
)
from .workouts_management import (
    cancel_workout,
    cancel_workout_for_sportsmans,
    complete_workout,
    complete_workout_for_sportsmans,
    get_workout_statuses,
    start_workout,
    start_workout_for_sportsmans,
)
from .workouts_pool import (
    create_workout_pool,
    delete_workout_pool,
    get_workout_pool,
    get_workouts_pool,
    update_workout_pool,
)
