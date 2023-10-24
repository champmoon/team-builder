from enum import IntEnum


class ExercisesTypesEnum(IntEnum):
    REST = 1
    WARM_UP = 2
    PUSH_UPS = 3
    PULL_UPS = 4
    SQUATS = 5
    BURPEE = 6


EXERCISES_TYPES_DESC: dict[ExercisesTypesEnum, str] = {
    ExercisesTypesEnum.REST: "Отдых",
    ExercisesTypesEnum.WARM_UP: "Разминка",
    ExercisesTypesEnum.PUSH_UPS: "Отжимания",
    ExercisesTypesEnum.PULL_UPS: "Подтягивания",
    ExercisesTypesEnum.SQUATS: "Приседания",
    ExercisesTypesEnum.BURPEE: "Бёрпи",
}
