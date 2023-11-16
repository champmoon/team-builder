from enum import IntEnum


class WorkoutsStatusesEnum(IntEnum):
    PLANNED = 1
    IN_PROGRESS = 2
    COMPLETED = 3


WORKOUTS_STATUSES_DESC = {
    WorkoutsStatusesEnum.PLANNED: "Запланирована",
    WorkoutsStatusesEnum.IN_PROGRESS: "В процессе",
    WorkoutsStatusesEnum.COMPLETED: "Завершена",
}
