from typing import TypeAlias

from .admins import AdminsRepository
from .exercises import ExercisesRepository
from .exercises_types import ExercisesTypesRepository
from .groups import GroupsRepository
from .sessions import SessionsRepository
from .sportsmans import SportsmansRepository
from .sportsmans_groups import SportsmansGroupsRepository
from .teams import TeamsRepository
from .trainers import TrainersRepository
from .workouts import WorkoutsRepository
from .sportsmans_workouts import SportsmansWorkoutsRepository
from .trainers_workouts import TrainersWorkoutsRepository
from .workouts_statuses import WorkoutsStatusesRepository
from .tgs_workouts import TGSWorkoutsRepository

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
