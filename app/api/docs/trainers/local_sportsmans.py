from ..base_docs import Docs

get_local_sportsmans: Docs = {
    "summary": "Получение всех фейков",
    "description": """
    ```
    Query Params:
        id - ID фейка(uuid)(required=false)

    Auth:
        Этот запрос доступен только тренерам.

    P.S:
        Если присылается id - возвращается фейк или 404
        Если без id - присылваются все фейка.

        Спортсменов с почтой вы тут не увидите.
    """,
    "responses": {
        200: {
            "description": "Получение всех фейков",
            "content": {
                "application/json": {
                    "example": [{
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "firstName": "string",
                        "middleName": "string",
                        "lastName": "string",
                        "teamId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    }]
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
            "description": "Фейк не найден",
            "content": {"application/json": {"example": {}}},
        },
    },
}


create_local_sportsmans: Docs = {
    "summary": "Создание фейка",
    "description": """
    ```
    Request Body:
        firstName - имя.
                    (str)

        middleName - фамилия.
                    (str)(required=false)

        lastName - отчество.
                    (str)(required=false)


    Auth:
        Этот запрос доступен только тренерам.

    P.S.
        Для создания фейка обязательно только имя,
        он автоматически подвяжется к команде тренера.
    """,
    "responses": {
        201: {
            "description": "Создана группа тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "firstName": "string",
                        "middleName": "string",
                        "lastName": "string",
                        "teamId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
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


update_local_sportsman: Docs = {
    "summary": "Обновление фейка",
    "description": """
    ```
    Query Params:
        id - ID фейка.
             (uuid)

    Request Body:
        firstName - имя.
                    (str)required=false)

        middleName - фамилия.
                    (str)(required=false)

        lastName - отчество.
                    (str)(required=false)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получен обновлённый фейк",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "firstName": "string",
                        "middleName": "string",
                        "lastName": "string",
                        "teamId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
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
            "description": "Фейк не найдена",
            "content": {"application/json": {"example": {}}},
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


delete_local_sportsmans: Docs = {
    "summary": "Удаление фейка",
    "description": """
    ```
    Query Params:
        id - ID фейка.
             (uuid)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получен удаленный фейк",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "firstName": "string",
                        "middleName": "string",
                        "lastName": "string",
                        "teamId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
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
            "description": "Фейк не найдена",
            "content": {"application/json": {"example": {}}},
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


merge_local_sportsman: Docs = {
    "summary": "Мердж фейка с тру спортиком",
    "description": """
    ```
    Request Body:
        localSportmanId - UUID фейка.
                          (UUID)

        email - почта настоящего.
                (str)

    Auth:
        Этот запрос доступен только тренерам.

     P.S:
        Этот запрос перезатираем фейка на настоящего,
        т.е. все тренировки, группы, история фейка станут
        тренировками, группами, историем тру.
        Фейк будет удален.

        И фейк, и тру должны быть в одной команде, если нет, то 404.
    """,
    "responses": {
        200: {
            "description": "Получен тру",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "true@true",
                        "firstName": "string",
                        "middleName": "string",
                        "lastName": "string",
                        "teamId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
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
            "description": "Фейк/тру не найдена",
            "content": {"application/json": {"example": {}}},
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
