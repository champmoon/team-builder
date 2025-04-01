tags_mapper = {
    "general_auth": "Авторизация",
    "general_registration": "Регистрация",
    "general_password": "Сброс пароля",
    "general_workouts": "Тренировки",
    "general_exercises": "Типы упражнения",
    "general_workouts_statuses": "Cтатусы тренировок",
    #
    # "trainers_auth": "Тренеры → Регистрация",
    "trainers_local_sportsmans": "Тренеры → Локальные спортсмены",
    "trainers_profile": "Тренеры → Профиль",
    "trainers_surveys": "Тренеры → Анкета",
    "trainers_teams": "Тренеры → Команда",
    "trainers_groups": "Тренеры → Группа",
    "trainers_exercises": "Тренеры → Типы упражнения",
    "trainers_workouts": "Тренеры → Тренировка",
    "trainers_workouts_management": "Тренеры → Управление тренировкой",
    "trainers_workouts_pool": "Тренеры → Программа тренировок",
    "trainers_stress_questionnaires": "Тренеры → Опросник по нагрузке",
    "trainers_health_questionnaires": "Тренеры → Опросник по здоровью",
    #
    # "sportsmans_auth": "Спортсмены → Регистрация",
    "sportsmans_profile": "Спортсмены → Профиль",
    "sportsmans_surveys": "Спортсмены → Анкета",
    "sportsmans_teams": "Спортсмены → Команда",
    "sportsmans_groups": "Спортсмены → Группа",
    "sportsmans_workouts": "Спортсмены → Тренировка",
    "sportsmans_workouts_management": "Спортсмены → Управление тренировкой",
    "sportsmans_stress_questionnaires": "Cпортсмены → Опросник по нагрузке",
    "sportsmans_health_questionnaires": "Cпортсмены → Опросник по здоровью",
}


openapi_tags = [{"name": tag_value} for tag_value in tags_mapper.values()]
