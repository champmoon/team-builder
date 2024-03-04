from ..base_docs import Docs

register_sportsman: Docs = {
    "summary": "Регистрация спортсмена",
    "description": """
    ```
    Request Body:
        email - почта спортсмена.
                (string)

        password - пароль тренера.
                   (string)(5 <= len <= 30)

        first_name - имя тренера.
               (string)(required=False)

        middle_name - фамилия тренера.
               (string)(required=False)

        last_name - отчество тренера.
               (string)(required=False)

        trainerID - ID тренера.(uuid)

    Auth:
        Этот запрос публичный.
    """,
    "responses": {
        201: {
            "description": "Успешная регистрация нового спортсмена.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "20c07d0a-f5dd-40c7-aa65-8ff9c12f4d96",
                        "email": "sportsman@sportsman.com",
                        "firstName": "string",
                        "middleName": "string",
                        "lastName": "string",
                        "teamId": "f4a6b819-1374-4692-977d-d8a976cf4ea9",
                    }
                },
            },
        },
        409: {
            "description": "Спортсмен с таким `email` уже существует.",
            "content": {
                "application/json": {
                    "example": {"detail": "Sportsman with email {email} already exists"}
                }
            },
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр был передан неверно.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "string_too_long",
                                "loc": ["body", "password"],
                                "msg": "String should have at most 100 characters",
                                "input": "password" * 12,
                                "ctx": {"max_length": 100},
                                "url": (
                                    "https://errors.pydantic.dev/2.3/v/string_too_long"
                                ),
                            }
                        ]
                    }
                }
            },
        },
        423: {
            "description": "Почта не была подтверждена.",
            "content": {
                "application/json": {
                    "example": {"detail": "Sportsman with email {email} not confirmed"}
                }
            },
        },
    },
}


confirm_sportsman_email: Docs = {
    "summary": "Подтверждение email спортсмена.",
    "description": """
    ```
    Query Params:
        confirm_token - токен для идентификации пользователя.(uuid)

    P.S.:
        Этот запрос служит для проверки почты пользователя.
        При регистрации на посту отправляется ссылка на confirm_email
        уже с confirm_token, который хранит информацию про пользователя.

        Ссылка активна 5 минут, после этого она протухает.

        При успешном ответе возвращается почта,
        которая автоматически подставляется в дальнейшую форму регистрации.
    """,
    "responses": {
        200: {
            "description": "Почта спортсмена подтверждена.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "20c07d0a-f5dd-40c7-aa65-8ff9c12f4d96",
                        "email": "sportsman@sportsman.com",
                        "firstName": "string",
                        "middleName": "string",
                        "lastName": "string",
                        "teamId": "f4a6b819-1374-4692-977d-d8a976cf4ea9",
                    }
                }
            },
        },
        410: {
            "description": (
                "По ссылке уже перешли, либо ссылка протухла, либо `confirm_token`"
                " изменили."
            ),
            "content": {"application/json": {"example": {"detail": "Gone"}}},
        },
        422: {
            "description": "Ошибка валидации, например `confirm_token`.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "uuid_parsing",
                                "loc": ["query", "confirm_token"],
                                "msg": (
                                    "Input should be a valid UUID, invalid group count:"
                                    " expected 5, found 3"
                                ),
                                "input": "702d2c4f-d2ac-",
                                "ctx": {
                                    "error": "invalid group count: expected 5, found 3"
                                },
                                "url": "https://errors.pydantic.dev/2.3/v/uuid_parsing",
                            }
                        ]
                    }
                }
            },
        },
    },
}


send_confirm_sportsman_email: Docs = {
    "summary": "Отправка подтверждающего email спортсмену.",
    "description": """
    ```
    Request Body:
        email - почта тренера.
                (string)

    P.S.:
        Этот запрос доступен только ТРЕНЕРАМ.

        Перед началом регистрации пользователю необходимо подтвердить свою почту.

        Этот запрос служит для отправки подтверждающей ссылки пользователю.
        При регистрации на почту отправляется ссылка на email
        уже с confirm_token, который хранит информацию про пользователя.

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
                    "example": {
                        "detail": {"msg": "email already sended", "expire": 295}
                    }
                }
            },
        },
        409: {
            "description": "Спортсмен с таким `email` уже существует.",
            "content": {
                "application/json": {
                    "example": {"detail": "Sportsman with email {email} already exists"}
                }
            },
        },
        422: {
            "description": "Ошибка валидации.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
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
                            }
                        ]
                    }
                }
            },
        },
    },
}
