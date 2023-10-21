tags_mapper = {
    "auth": "Авторизация / регистрация для тренеров / спортсменов",
    ...: ...,  # noqa
    "trainers_profile": "Тренеры → Профиль",
    "sportsmans_profile": "Спортсмены → Профиль",
    ...: ...,  # noqa
    "trainers_teams": "Тренеры → Команды",
    "sportsmans_teams": "Спортсмены → Команды",
    ...: ...,  # noqa
    "trainers_groups": "Тренеры → Группы",
    "sportsmans_groups": "Спортсмены → Группы",
}


openapi_tags = [{"name": tag_value} for tag_value in tags_mapper.values()]
