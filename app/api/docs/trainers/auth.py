from ..base_docs import Docs

register_trainer: Docs = {
    "summary": "Регистрация тренера",
    "description": """
    ```
    Request Body:
        email - почта тренера.
                (string)

        password - пароль тренера.
                   (string)(5 <= len <= 30)

        first_name - имя тренера.
               (string)(required=False)

        middle_name - фамилия тренера.
               (string)(required=False)

        last_name - отчество тренера.
               (string)(required=False)

    Auth:
        Этот запрос публичный.
    """,
    "responses": {
        201: {
            "description": "Успешная регистрация нового тренера.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "c5300a69-ec99-473e-9df5-6b9c2db64eb9",
                        "email": "trainer@trainer.com",
                        "firstName": "string",
                        "lastName": "string",
                    }
                },
            },
        },
        409: {
            "description": "Тренер с таким `email` уже существует.",
            "content": {
                "application/json": {
                    "example": {"detail": "Trainer with email {email} already exists"}
                }
            },
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр был передан неверно.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_too_long",
                            "loc": ["body", "password"],
                            "msg": "String should have at most 100 characters",
                            "input": "password" * 12,
                            "ctx": {"max_length": 100},
                            "url": "https://errors.pydantic.dev/2.3/v/string_too_long",
                        }]
                    }
                }
            },
        },
        423: {
            "description": "Почта не была подтверждена.",
            "content": {
                "application/json": {
                    "example": {"detail": "Trainer with email {email} not confirmed"}
                }
            },
        },
    },
}


confirm_trainer_email: Docs = {
    "summary": "Подтверждение email тренера.",
    "description": """
    ```
    Request Body:
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
            "description": "Почта тренера подтверждена.",
            "content": {
                "application/json": {
                    "example": {
                        "email": "trainer@trainer.com",
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
                        "detail": [{
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
                        }]
                    }
                }
            },
        },
    },
}


send_confirm_trainer_email: Docs = {
    "summary": "Отправка подтверждающего email тренеру.",
    "description": """
    ```
    Request Body:
        email - почта тренера.
                (string)

    P.S.:
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
                    "example": {"detail": {"detail": "email", "expire": 295}}
                }
            },
        },
        409: {
            "description": "Тренер с таким `email` уже существует.",
            "content": {"application/json": {"example": {"detail": "trainer"}}},
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
