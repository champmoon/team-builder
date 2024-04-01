# for migrations
from app.db.base_class import Base

from .admins import Admins
from .exercises import Exercises
from .exercises_types import ExercisesTypes
from .groups import Groups
from .questionnaires import StressQuestionnaires
from .sessions import Sessions
from .sportsmans import Sportsmans
from .sportsmans_groups import SportsmansGroups
from .sportsmans_workouts import SportsmansWorkouts
from .surveys import SportsmanSurveys, TeamSurveys
from .teams import Teams
from .tgs_workouts import TGSWorkouts
from .trainers import Trainers
from .trainers_workouts import TrainersWorkouts
from .workouts import Workouts, WorkoutsPool
from .workouts_statuses import WorkoutsStatuses
