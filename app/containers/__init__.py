from typing import Type

from .admins import AdminsContainer
from .auth import AuthContainer
from .base_class import BaseContainer
from .sessions import SessionsContainer
from .sportsmans import SportsmansContainer
from .trainers import TrainersContainer


class Containers:
    admins = AdminsContainer
    sportsmans = SportsmansContainer
    trainers = TrainersContainer
    sessions = SessionsContainer
    auth = AuthContainer

    @classmethod
    def get_all_containers(cls) -> list[Type[BaseContainer]]:
        containers = []
        for _, container_cls in vars(cls).items():
            try:
                if issubclass(container_cls, BaseContainer):
                    containers.append(container_cls)
            except TypeError:
                continue
        return containers


def wire_containers() -> None:
    for Container in Containers.get_all_containers():
        Container().wire(packages=[Container.wire_config])
