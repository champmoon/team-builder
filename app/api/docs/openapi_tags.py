tags_mapper = {
    "auth": "Авторизация / регистрация для тренеров / спортсменов",
    #
    "trainers_profile": "Тренеры → Профиль",
    "sportsmans_profile": "Спортсмены → Профиль",
    #
    "trainers_teams": "Тренеры → Команды",
    "sportsmans_teams": "Спортсмены → Команды",
    #
    "trainers_groups": "Тренеры → Группы",
    "sportsmans_groups": "Спортсмены → Группы",
}


openapi_tags = [{"name": tag_value} for tag_value in tags_mapper.values()]
