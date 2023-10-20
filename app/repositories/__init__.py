from typing import TypeAlias

from .admins import AdminsRepository
from .groups import GroupsRepository
from .sessions import SessionsRepository
from .sportsmans import SportsmansRepository
from .sportsmans_groups import SportsmansGroupsRepository
from .teams import TeamsRepository
from .trainers import TrainersRepository


class Repositories:
    admins: TypeAlias = AdminsRepository
    trainers: TypeAlias = TrainersRepository
    sportsmans: TypeAlias = SportsmansRepository
    sessions: TypeAlias = SessionsRepository
    teams: TypeAlias = TeamsRepository
    groups: TypeAlias = GroupsRepository
    sportsmans_groups: TypeAlias = SportsmansGroupsRepository
