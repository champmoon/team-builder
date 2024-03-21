tags_mapper = {
    "general_auth": "Авторизация",
    "general_exercises": "Упражнения",
    #
    "trainers_auth": "Тренеры → Регистрация",
    "trainers_profile": "Тренеры → Профиль",
    "trainers_surveys": "Тренеры → Анкета",
    "trainers_teams": "Тренеры → Команды",
    "trainers_groups": "Тренеры → Группы",
    "trainers_workouts": "Тренеры → Тренировки",
    "trainers_workouts_pool": "Тренеры → Программа тренировок",
    #
    "sportsmans_auth": "Спортсмены → Регистрация",
    "sportsmans_profile": "Спортсмены → Профиль",
    "sportsmans_surveys": "Спортсмены → Анкета",
    "sportsmans_teams": "Спортсмены → Команды",
    "sportsmans_groups": "Спортсмены → Группы",
}


openapi_tags = [{"name": tag_value} for tag_value in tags_mapper.values()]
