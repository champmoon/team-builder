from ..base_docs import Docs

get_self_groups: Docs = {
    "summary": "Получение всех групп спортсмена",
    "description": """
    ```
    Auth:
        Этот запрос доступен только спортсменам.
    """,
    "responses": {
        200: {
            "description": "Получены группы спортсмена",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "name": "string",
                            "sportsmans": [{
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "string",
                                "name": "string",
                            }],
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "name": "string",
                            "sportsmans": [{
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "string",
                                "name": "string",
                            }],
                        },
                    ]
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
    },
}


get_self_group: Docs = {
    "summary": "Получение группы спортсмена",
    "description": """
    ```
    Path Params:
        id - ID группы.
             (uuid)

    Auth:
        Этот запрос доступен только спортсменам.
    """,
    "responses": {
        200: {
            "description": "Получение группы спортсмена",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "string",
                        "sportsmans": [{
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "email": "string",
                            "name": "string",
                        }],
                    }
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "Группа не найдена",
            "content": {
                "application/json": {
                    "example": {"detail": "Group with id {id} not found"}
                }
            },
        },
        422: {
            "description": "Ошибка валидации, `id` невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["path", "id"],
                            "msg": "Input should be a valid string",
                            "input": 1,
                        }]
                    }
                }
            },
        },
    },
}


outs_off_groups: Docs = {
    "summary": "Выход из групп",
    "description": """
    ```
    Request Body:
        groupsIds - ID групп.
                    (array[uuid])

    Auth:
        Этот запрос доступен только спортсменам.

    P.S
        В ответе статуса 200 со спортсменом присылвается
        и его группы, но в группах уже нет удалённых
        "Невалидные" группы игнорируются
    """,
    "responses": {
        200: {
            "description": "Получена данные спортсмена с оставшиемися группами",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
                        "name": "string",
                        "teamId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "groups": [{
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "name": "string",
                        }],
                    },
                }
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        422: {
            "description": "Ошибка валидации, `id` невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["path", "id"],
                            "msg": "Input should be a valid string",
                            "input": 1,
                        }]
                    }
                }
            },
        },
        500: {
            "description": "Ошибка сервера: команды не существует",
            "content": {"application/json": {"example": {"detail": "Team must exist"}}},
        },
    },
}


out_off_group: Docs = {
    "summary": "Выход из групы",
    "description": """
    ```
    Path Params:
        id - ID группы.
             (uuid)

    Auth:
        Этот запрос доступен только спортсменам.

    P.S
        В ответе статуса 200 со спортсменом присылается
        и его группы, но в группах уже нет удалённой
    """,
    "responses": {
        200: {
            "description": "Получены данные спортсмена с оставшиемися группами",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
                        "name": "string",
                        "teamId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "groups": [{
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "name": "string",
                        }],
                    },
                }
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является тренером.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "Группа не найдена",
            "content": {
                "application/json": {
                    "example": {"detail": "Group with id {id} not found"}
                }
            },
        },
        422: {
            "description": "Ошибка валидации, `id` невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["path", "id"],
                            "msg": "Input should be a valid string",
                            "input": 1,
                        }]
                    }
                }
            },
        },
        500: {
            "description": "Ошибка сервера: команды не существует",
            "content": {"application/json": {"example": {"detail": "Team must exist"}}},
        },
    },
}
