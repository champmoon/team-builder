from typing import TypeAlias

from .admins import AdminsRepository
from .exercises import ExercisesRepository
from .exercises_types import ExercisesTypesRepository
from .groups import GroupsRepository
from .sessions import SessionsRepository
from .sportsmans import SportsmansRepository
from .sportsmans_groups import SportsmansGroupsRepository
from .sportsmans_workouts import SportsmansWorkoutsRepository
from .surveys import SportsmanSurveysRepository, TeamSurveysRepository
from .teams import TeamsRepository
from .tgs_workouts import TGSWorkoutsRepository
from .trainers import TrainersRepository
from .trainers_workouts import TrainersWorkoutsRepository
from .workouts import WorkoutsRepository, WorkoutsPoolRepository
from .workouts_statuses import WorkoutsStatusesRepository


class Repositories:
    admins: TypeAlias = AdminsRepository
    trainers: TypeAlias = TrainersRepository
    sportsmans: TypeAlias = SportsmansRepository
    sessions: TypeAlias = SessionsRepository
    teams: TypeAlias = TeamsRepository
    groups: TypeAlias = GroupsRepository
    sportsmans_groups: TypeAlias = SportsmansGroupsRepository
    exercises_types: TypeAlias = ExercisesTypesRepository
    workouts: TypeAlias = WorkoutsRepository
    exercises: TypeAlias = ExercisesRepository
    sportsmans_workouts: TypeAlias = SportsmansWorkoutsRepository
    trainers_workouts: TypeAlias = TrainersWorkoutsRepository
    workouts_statuses: TypeAlias = WorkoutsStatusesRepository
    tgs_workouts: TypeAlias = TGSWorkoutsRepository
    team_surveys: TypeAlias = TeamSurveysRepository
    sportsman_surveys: TypeAlias = SportsmanSurveysRepository
    workouts_pool: TypeAlias = WorkoutsPoolRepository
