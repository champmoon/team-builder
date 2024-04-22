from enum import IntEnum


class WorkoutsStatusesEnum(IntEnum):
    PLANNED = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    ACTIVE = 4
    CANCELED = 5


WORKOUTS_STATUSES_DESC = {
    WorkoutsStatusesEnum.PLANNED: "Запланирована",
    WorkoutsStatusesEnum.IN_PROGRESS: "В процессе",
    WorkoutsStatusesEnum.COMPLETED: "Завершена",
    WorkoutsStatusesEnum.ACTIVE: "Активна",
    WorkoutsStatusesEnum.CANCELED: "Отменена",
}
  