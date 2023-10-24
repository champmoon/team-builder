from enum import IntEnum


class ExercisesTypesEnum(IntEnum):
    REST = 1
    WARM_UP = 2
    HITCH = 3
    PUSH_UPS = 4
    PULL_UPS = 5
    SQUATS = 6
    BURPEE = 7


EXERCISES_TYPES_DESC: dict[ExercisesTypesEnum, str] = {
    ExercisesTypesEnum.REST: "Отдых",
    ExercisesTypesEnum.WARM_UP: "Разминка",
    ExercisesTypesEnum.HITCH: "Заминка",
    ExercisesTypesEnum.PUSH_UPS: "Отжимания",
    ExercisesTypesEnum.PULL_UPS: "Подтягивания",
    ExercisesTypesEnum.SQUATS: "Приседания",
    ExercisesTypesEnum.BURPEE: "Бёрпи",
}
