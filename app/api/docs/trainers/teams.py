from ..base_docs import Docs

get_self_team: Docs = {
    "summary": "Получение команды тренера",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получена команда тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
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
    },
}


send_invite_sportsman_to_team: Docs = {
    "summary": "Отправка на почту спортсмена ссылки на команду",
    "description": """
    ```
    Request Body:
        email - почта спортсмена.
                (string)

        localSportsmanId - это id локального спортмена.
                           (UUID)(required=false)

    Auth:
        Этот запрос доступен только тренерам.
    P.S
        На почту спортсмена прилетит ссылка на добавление в команду.
        Если указать localSportsmanId, то когда спортсмен добавится в команду,
        он смерджится с добавленным.

        Ссылка активна 5 минут, после этого она протухает.

        expire - время, через которое ссылка протухнет(секунды).

    DEBUG:
        Для DEBUG версии ссылка будет возвращатсья в запросе, на почту ничего
        отправлять не будет. Пример можно посмотреть ниже.
    """,
    "responses": {
        202: {
            "description": "Письмо на `email` успешно отправлено.",
            "content": {
                "application/json": {
                    "examples": {
                        "not_debug": {
                            "summary": "Запрос с отправлением на `email`",
                            "description": "Этот запрос отправляет письмо на почту",
                            "value": {"expire": 300},
                        },
                        "debug": {
                            "summary": "DEBUG версия",
                            "description": (
                                "Этот запрос сразу возвращает `uri` на подтверждение"
                            ),
                            "value": {
                                "uri": "http://192.168.22.169:9000/register?confirm_token=7a32cb4c-ed9b-41c3-a8e1-7a95ab074e94",
                                "expire": 300,
                            },
                        },
                    }
                }
            },
        },
        403: {
            "description": (
                "Письмо на `email` уже было отправлено, следующая отправка доступна"
                " через `time` секунд."
            ),
            "content": {
                "application/json": {
                    "example": {"detail": {"detail": "email", "expire": 295}}
                }
            },
        },
        404: {
            "description": "Спортсмена нет",
            "content": {"application/json": {"example": {}}},
        },
        409: {
            "description": "Спортсмен уже в другой команде",
            "content": {"application/json": {"example": {}}},
        },
        422: {
            "description": "Ошибка валидации.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "value_error",
                            "loc": ["body", "email"],
                            "msg": (
                                "value is not a valid email address: The part after"
                                " the @-sign is not valid. It should have a period."
                            ),
                            "input": "invalid@example",
                            "ctx": {
                                "reason": (
                                    "The part after the @-sign is not valid. It"
                                    " should have a period."
                                )
                            },
                        }]
                    }
                }
            },
        },
    },
}


create_invite_link: Docs = {
    "summary": "Создать ссылку приглашения в команду",
    "description": """
    ```

    Auth:
        Этот запрос доступен только тренерам.
    P.S
        Ссылка активна 5 минут, после этого она протухает.
    """,
    "responses": {
        200: {
            "description": "Ссылка на команду",
            "content": {
                "application/json": {
                    "example": {
                        "link": "http://localhost:5000/invite?confirm_token=c8909c00-66e4-405f-bd57-9942512b3d19"
                    }
                },
            },
        },
    },
}


adds_sportsmans_to_team: Docs = {
    "summary": "Добавление спортсменов в команду",
    "description": """
    ```
    Request Body:
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
            "description": "Получена обновлённая команда тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportType": "rugby",
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


kick_sportsman_off_team: Docs = {
    "summary": "Удаление спортсмена из команду",
    "description": """
    ```
    Request Body:
        sportsmanEmail - почта спортсмена.
                         (string)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получена обновлённая команда тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "sportType": "rugby",
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
            "description": "Удаляемый спортсмен не найден.",
            "content": {"application/json": {"example": {"detail": "sportsman"}}},
        },
        409: {
            "description": "Удаляемый спортсмен не состоит в этой команде",
            "content": {"application/json": {"example": {"detail": "sportsman"}}},
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


kicks_sportsmans_off_team: Docs = {
    "summary": "Удаление спортсменов из команду",
    "description": """
    ```
    Request Body:
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
            "description": "Получена обновлённая команда тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "trainerId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
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
