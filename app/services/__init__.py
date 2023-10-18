from typing import TypeAlias

from .admins import AdminsService
from .auth import AuthService
from .sessions import SessionsService
from .sportsmans import SportsmansService
from .trainers import TrainersService


class Services:
    admins: TypeAlias = AdminsService
    sportsmans: TypeAlias = SportsmansService
    trainers: TypeAlias = TrainersService
    sessions: TypeAlias = SessionsService
    auth: TypeAlias = AuthService
