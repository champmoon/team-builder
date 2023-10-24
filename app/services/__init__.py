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
