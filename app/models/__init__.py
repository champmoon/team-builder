# for migrations
from app.db.base_class import Base

from .admins import Admins
from .exercises import Exercises
from .exercises_types import ExercisesTypes
from .groups import Groups
from .sessions import Sessions
from .sportsmans import Sportsmans
from .sportsmans_groups import SportsmansGroups
from .sportsmans_trainigs import SportsmansTrainigs
from .teams import Teams
from .trainers import Trainers
from .trainigs import Trainigs
from .trainigs_statuses import TrainigsStatuses
