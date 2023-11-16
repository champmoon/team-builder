# for migrations
from app.db.base_class import Base

from .admins import Admins
from .exercises import Exercises
from .exercises_types import ExercisesTypes
from .groups import Groups
from .sessions import Sessions
from .sportsmans import Sportsmans
from .sportsmans_groups import SportsmansGroups
from .sportsmans_workouts import SportsmansWorkouts
from .teams import Teams
from .trainers import Trainers
from .workouts import Workouts
from .workouts_statuses import WorkoutsStatuses
from .trainers_workouts import TrainersWorkouts
from .teams_groups_workouts import TeamsGroupsWorkouts 
