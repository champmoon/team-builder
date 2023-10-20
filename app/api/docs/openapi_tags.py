tags_mapper = {
    "auth": "Авторизация / регистрация для тренеров / спортсменов",
    ...: ...,
    "trainers_teams": "Тренеры → Команды",
    "trainers_groups": "Тренеры → Группы",
    "sportsmans_teams": "Спортсмены → Команды",
}


openapi_tags = [
    {
        "name": tags_mapper["auth"],
        "description": "Запросы для авторизацию/регистрацию тренеров / спортсменов",
    },
    {
        "name": tags_mapper["trainers_teams"],
        "description": "",
    },
    {
        "name": tags_mapper["trainers_groups"],
        "description": "",
    },
    {
        "name": tags_mapper["sportsmans_teams"],
        "description": "",
    },
]
