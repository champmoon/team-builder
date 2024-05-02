tags_mapper = {
    "general_auth": "Авторизация",
    "general_exercises": "Упражнения",
    #
    "trainers_auth": "Тренеры → Регистрация",
    "trainers_profile": "Тренеры → Профиль",
    "trainers_surveys": "Тренеры → Анкета",
    "trainers_teams": "Тренеры → Команда",
    "trainers_groups": "Тренеры → Группа",
    "trainers_workouts": "Тренеры → Тренировка",
    "trainers_workouts_pool": "Тренеры → Программа тренировок",
    "trainers_stress_questionnaires": "Тренеры → Опросник по нагрузке",
    "trainers_health_questionnaires": "Тренеры → Опросник по здоровью",
    #
    "sportsmans_auth": "Спортсмены → Регистрация",
    "sportsmans_profile": "Спортсмены → Профиль",
    "sportsmans_surveys": "Спортсмены → Анкета",
    "sportsmans_teams": "Спортсмены → Команда",
    "sportsmans_groups": "Спортсмены → Группа",
    "sportsmans_workouts": "Спортсмены → Тренировка",
    "sportsmans_stress_questionnaires": "Cпортсмены → Опросник по нагрузке",
    "sportsmans_health_questionnaires": "Cпортсмены → Опросник по здоровью",
}


openapi_tags = [{"name": tag_value} for tag_value in tags_mapper.values()]
