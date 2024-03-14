from typing import TypeAlias

from .admins import AdminsService
from .auth import AuthService
from .exercises import ExercisesService
from .exercises_types import ExercisesTypesService
from .groups import GroupsService
from .sessions import SessionsService
from .sportsmans import SportsmansService
from .sportsmans_groups import SportsmansGroupsService
from .sportsmans_workouts import SportsmansWorkoutsService
from .surveys import SportsmanSurveysService, TeamSurveysService
from .teams import TeamsService
from .tgs_workouts import TGSWorkoutsService
from .trainers import TrainersService
from .trainers_workouts import TrainersWorkoutsService
from .workouts import WorkoutsService, WorkoutsPoolService
from .workouts_statuses import WorkoutsStatusesService


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
    tgs_workouts: TypeAlias = TGSWorkoutsService
    team_surveys: TypeAlias = TeamSurveysService
    sportsman_surveys: TypeAlias = SportsmanSurveysService
    workouts_pool: TypeAlias = WorkoutsPoolService
