from typing import TypeAlias

from .admins import AdminsService
from .auth import AuthService
from .exercises_types import ExercisesTypesService
from .groups import GroupsService
from .sessions import SessionsService
from .sportsmans import SportsmansService
from .sportsmans_groups import SportsmansGroupsService
from .teams import TeamsService
from .trainers import TrainersService
from .trainers_workouts import TrainersWorkoutsService
from .workouts import WorkoutsService
from .exercises import ExercisesService
from .sportsmans_workouts import SportsmansWorkoutsService
from .workouts_statuses import WorkoutsStatusesService
from .teams_groups_workouts import TeamsGroupsWorkoutsService


class Services:
    admins: TypeAlias = AdminsService
    sportsmans: TypeAlias = SportsmansService
    trainers: TypeAlias = TrainersService
    sessions: TypeAlias = SessionsService
    auth: TypeAlias = AuthService
    teams: TypeAlias = TeamsService
    groups: TypeAlias = GroupsService
    sportsmans_groups: TypeAlias = SportsmansGroupsService
    exercises_types: TypeAlias = ExercisesTypesService
    trainers_workouts: TypeAlias = TrainersWorkoutsService
    workouts: TypeAlias = WorkoutsService
    exercises: TypeAlias = ExercisesService
    sportsmans_workouts: TypeAlias = SportsmansWorkoutsService
    workouts_statuses: TypeAlias = WorkoutsStatusesService
    teams_groups_workouts: TypeAlias = TeamsGroupsWorkoutsService
