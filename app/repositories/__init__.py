from typing import TypeAlias

from .admins import AdminsRepository
from .sessions import SessionsRepository
from .sportsmans import SportsmansRepository
from .trainers import TrainersRepository


class Repositories:
    admins: TypeAlias = AdminsRepository
    trainers: TypeAlias = TrainersRepository
    sportsmans: TypeAlias = SportsmansRepository
    sessions: TypeAlias = SessionsRepository
