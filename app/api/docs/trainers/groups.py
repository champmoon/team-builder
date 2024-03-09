from ..base_docs import Docs

get_self_groups: Docs = {
    "summary": "Получение всех групп тренера",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получение всех групп тренера",
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
    "summary": "Получение группы тренера",
    "description": """
    ```
    Path Params:
        id - ID группы.
             (uuid)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получение группы тренера",
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


create_group: Docs = {
    "summary": "Создание группы",
    "description": """
    ```
    Request Body:
        name - имя группы.
               (uuid)

        sportsmansEmails - почты спортсмена.
                           (array[string])(required=false)

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        При создании группы можно сразу указать спорсменов,
        которые будут в новой команде.
    """,
    "responses": {
        200: {
            "description": "Создана группа тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "string",
                        "sportsmans": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "first@sportsman.com",
                                "name": "first",
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "second@sportsman.com",
                                "name": "second",
                            },
                        ],
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
        422: {
            "description": "Ошибка валидации, какой-ир параметр невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["body", "name"],
                            "msg": "Input should be a valid string",
                            "input": 1,
                        }]
                    }
                }
            },
        },
    },
}


update_group: Docs = {
    "summary": "Обновление группы тренера",
    "description": """
    ```
    Path Params:
        id - ID группы.
             (uuid)

    Request Body:
        name - имя тренера.
               (string)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получена обновлённая группы тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "haha3times",
                        "sportsmans": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "first@sportsman.com",
                                "name": "first",
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "second@sportsman.com",
                                "name": "second",
                            },
                        ],
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
            "description": "Ошибка валидации, какой-то параметр невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["body", "name"],
                            "msg": "Input should be a valid string",
                            "input": 1,
                        }]
                    }
                }
            },
        },
    },
}


delete_group: Docs = {
    "summary": "Удаление группы тренера",
    "description": """
    ```
    Path Params:
        id - ID группы.
             (uuid)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Группы тренера успешно удалена",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "haha3times",
                        "sportsmans": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "first@sportsman.com",
                                "name": "first",
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "second@sportsman.com",
                                "name": "second",
                            },
                        ],
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


add_sportsman_to_group: Docs = {
    "summary": "Добавление спортсмена в группу",
    "description": """
    ```
    Request Body:
        groupId - ID группы.
                  (uuid)

        sportsmanEmail - почта спортсмена.
                         (string)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получена обновлённая группа тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "haha3times",
                        "sportsmans": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "first@sportsman.com",
                                "name": "first",
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "second@sportsman.com",
                                "name": "second",
                            },
                        ],
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
            "description": "Какой-то ресурс не найден",
            "content": {
                "application/json": {
                    "examples": {
                        "group": {
                            "summary": "Группа не найдена",
                            "value": {"detail": "Group with id {groupId} not found"},
                        },
                        "sportsman": {
                            "summary": "Спортсмен не найден",
                            "value": {
                                "detail": (
                                    "Sportsman with email {sportsmanEmail} not be on a"
                                    " team"
                                )
                            },
                        },
                    }
                }
            },
        },
        409: {
            "description": "Cпортсмен не состоит в команде тренера",
            "content": {
                "application/json": {
                    "example": {
                        "detail": (
                            "Sportsman with email {sportsman_email} not be on a team"
                        )
                    }
                }
            },
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["body", "name"],
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


adds_sportsmans_to_group: Docs = {
    "summary": "Добавление спортсменов в группы",
    "description": """
    ```
    Request Body:
        groupId - ID группы.
                  (uuid)
        sportsmansEmails - почты спортсмена.
                           (array[string])

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Этот запрос позволяет сразу добавить несколько спортсменов.
        Однако тут игнорируются ошибки по каждому спортсмену.
        Добавляются только "валидные" спортсмены.

    """,
    "responses": {
        200: {
            "description": "Получена обновлённая группа тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "haha3times",
                        "sportsmans": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "first@sportsman.com",
                                "name": "first",
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "second@sportsman.com",
                                "name": "second",
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "email": "third@sportsman.com",
                                "name": "third",
                            },
                        ],
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
                    "example": {"detail": "Group with id {group_id} not found"}
                }
            },
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["body", "name"],
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


kick_sportsman_off_group: Docs = {
    "summary": "Удаление спортсмена из группы",
    "description": """
    ```
    Request Body:
        groupid - ID группы.
                  (uuid)
        sportsmanEmail - почта спортсмена.
                         (string)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получена обновлённая группа тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "haha3times",
                        "sportsmans": [{
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "email": "first@sportsman.com",
                            "name": "first",
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
            "description": "Какой-то ресурс не найден",
            "content": {
                "application/json": {
                    "examples": {
                        "group": {
                            "summary": "Группа не найдена",
                            "value": {"detail": "Group with id {groupId} not found"},
                        },
                        "sportsman": {
                            "summary": "Спортсмен не найден",
                            "value": {
                                "detail": (
                                    "Sportsman with email {sportsmanEmail} not be on a"
                                    " team"
                                )
                            },
                        },
                    }
                }
            },
        },
        409: {
            "description": "Удаляемый спортсмен не состоит в этой команде",
            "content": {
                "application/json": {
                    "example": {
                        "detail": (
                            "Sportsman with email {sportsmanEmail} not be on a team"
                        )
                    }
                }
            },
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["body", "name"],
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


kicks_sportsmans_off_group: Docs = {
    "summary": "Удаление спортсменов из группы",
    "description": """
    ```
    Request Body:
        groupid - ID группы.
                  (uuid)
        sportsmansEmails - почты спортсмена.
                           (array[string])

    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Этот запрос позволяет сразу удалять несколько спортсменов.
        Однако тут игнорируются ошибки по каждому спортсмену.
        Удаляются только "валидные" спортсмены.

    """,
    "responses": {
        200: {
            "description": "Получена обновлённая группы тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "haha3times",
                        "sportsmans": [],
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
                    "example": {"detail": "Group with id {group_id} not found"}
                }
            },
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["body", "name"],
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
