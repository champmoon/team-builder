from typing import Type

from .admins import AdminsContainer
from .auth import AuthContainer
from .base_class import BaseContainer
from .exercises_types import ExercisesTypesContainer
from .groups import GroupsContainer
from .sessions import SessionsContainer
from .sportsmans import SportsmansContainer
from .sportsmans_groups import SportsmansGroupsContainer
from .teams import TeamsContainer
from .trainers import TrainersContainer
from .workouts import WorkoutContainer
from .exercises import ExercisesContainer
from .workouts_statuses import WorkoutsStatusesContainer
from .sportsmans_workouts import SportsmansWorkoutsContainer
from .trainers_workouts import TrainersWorkoutsContainer
from .teams_groups_workouts import TeamsGroupsWorkoutsContainer


class Containers:
    admins = AdminsContainer
    sportsmans = SportsmansContainer
    trainers = TrainersContainer
    sessions = SessionsContainer
    auth = AuthContainer
    teams = TeamsContainer
    groups = GroupsContainer
    sportsmans_groups = SportsmansGroupsContainer
    exercises_types = ExercisesTypesContainer
    workouts = WorkoutContainer
    exercises = ExercisesContainer
    workouts_statuses = WorkoutsStatusesContainer
    sportsmans_workouts = SportsmansWorkoutsContainer
    trainers_workouts = TrainersWorkoutsContainer
    teams_groups_workouts = TeamsGroupsWorkoutsContainer

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
