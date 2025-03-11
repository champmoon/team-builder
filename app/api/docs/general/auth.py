from ..base_docs import Docs

login: Docs = {
    "summary": "Авторизация тренера / спортсмена / админа",
    "description": """
    ```
    Request Body:
        email - почта тренера / спортсмена.
                (string)

        password - пароль тренера / спортсмена.
                   (string)(5 <= len <= 30)

        rememberMe - флаг продления refresh токена.
                     (bool)(default=false)
                     Если false - refresh живет 1 день.
                     Если true - 1 месяц

    Auth:
        Этот запрос публичный.
    """,
    "responses": {
        200: {
            "description": (
                "Успешная авторизация нового спортсмена, получение пары `jwt"
                " access/refresh токенов`."
            ),
            "content": {
                "application/json": {
                    "examples": {
                        "trainer": {
                            "summary": "Авторизация тренера",
                            "value": {
                                "accessToken": (
                                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                    ".eyJleHAiOjE2OTkzNDExMjAsInN1YiI6IntcInVzZXJfaWRcIjogXCIxZTcyNDg0YS0yYmRkLTQ2MzAtOGQ2Yy1iOGNiN2I0Mjk3ZDFcIiwgXCJncm91cFwiOiBcInVzZXJcIn0ifQ"
                                    ".eVygh9rRrwcPd46a9V9mhznhJh87Nt13LxwN17un_Us"
                                ),
                                "refreshToken": "cfb4d589-88b1-474b-8645-3c5a4f53c32c",
                                "userType": "trainer",
                            },
                        },
                        "sportsman": {
                            "summary": "Авторизация спортсмена",
                            "value": {
                                "accessToken": (
                                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                    ".eyJleHAiOjE2OTkzNDExMjAsInN1YiI6IntcInVzZXJfaWRcIjogXCIxZTcyNDg0YS0yYmRkLTQ2MzAtOGQ2Yy1iOGNiN2I0Mjk3ZDFcIiwgXCJncm91cFwiOiBcInVzZXJcIn0ifQ"
                                    ".eVygh9rRrwcPd46a9V9mhznhJh87Nt13LxwN17un_Us"
                                ),
                                "refreshToken": "cfb4d589-88b1-474b-8645-3c5a4f53c32c",
                                "userType": "sportsman",
                            },
                        },
                        "admin": {
                            "summary": "Авторизация админа",
                            "value": {
                                "accessToken": (
                                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                    ".eyJleHAiOjE2OTkzNDExMjAsInN1YiI6IntcInVzZXJfaWRcIjogXCIxZTcyNDg0YS0yYmRkLTQ2MzAtOGQ2Yy1iOGNiN2I0Mjk3ZDFcIiwgXCJncm91cFwiOiBcInVzZXJcIn0ifQ"
                                    ".eVygh9rRrwcPd46a9V9mhznhJh87Nt13LxwN17un_Us"
                                ),
                                "refreshToken": "cfb4d589-88b1-474b-8645-3c5a4f53c32c",
                                "userType": "admin",
                            },
                        },
                    }
                }
            },
        },
        404: {
            "description": "Тренер / спортсмен с таким `email` не найден.",
            "content": {"application/json": {"example": {"detail": "user"}}},
        },
        409: {
            "description": "Неверный `password`.",
            "content": {"application/json": {"example": {"detail": "user"}}},
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
    },
}


logout: Docs = {
    "summary": "Выход с аккаунта тренера / спортсмена / админа",
    "description": """
    ```
    Request Body:
        refreshToken - рефреш токен авторизации.
                       (uuid)

    Auth:
        Этот запрос требует авторизации любого типа пользователей.

    P.S.
        accessToken передаётся в хедере - Authorization: Bearer <accessToken>,
        как и во всех запросах, требующих авторизации.

        Этот запрос удаляет переданный refreshToken,
        поэтому по данному токену не пройдёт запрос /refresh

        Однако accessToken будет валиден ещё час, поэтому при запросе /logout
        надо очищать все токены на стороне клиента.
    """,
    "responses": {
        200: {
            "description": "`accessToken` валидный.",
            "content": {"application/json": {"example": {}}},
        },
        401: {
            "description": "`accessToken` не был передан, или просросен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        404: {
            "description": "`refreshToken` не был найден в БД.",
            "content": {"application/json": {"example": {"detail": "refresh_token"}}},
        },
        422: {
            "description": "Ошибка валидации, `refreshToken` невалидный.",
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
    },
}


refresh: Docs = {
    "summary": "Получение новой пары токенов с помощью refreshToken.",
    "description": """
    ```
    Request Body:
        refreshToken - refresh токен авторизации.
                       (uuid)

    Auth:
        Этот запрос публичный.
    """,
    "responses": {
        201: {
            "description": "`refreshToken` валидный. Получена новая пара токенов.",
            "content": {
                "application/json": {
                    "examples": {
                        "trainer": {
                            "summary": "Refresh тренера",
                            "value": {
                                "accessToken": (
                                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                    ".eyJleHAiOjE2OTkzNDExMjAsInN1YiI6IntcInVzZXJfaWRcIjogXCIxZTcyNDg0YS0yYmRkLTQ2MzAtOGQ2Yy1iOGNiN2I0Mjk3ZDFcIiwgXCJncm91cFwiOiBcInVzZXJcIn0ifQ"
                                    ".eVygh9rRrwcPd46a9V9mhznhJh87Nt13LxwN17un_Us"
                                ),
                                "refreshToken": "cfb4d589-88b1-474b-8645-3c5a4f53c32c",
                                "userType": "trainer",
                            },
                        },
                        "sportsman": {
                            "summary": "Refresh спортсмена",
                            "value": {
                                "accessToken": (
                                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                    ".eyJleHAiOjE2OTkzNDExMjAsInN1YiI6IntcInVzZXJfaWRcIjogXCIxZTcyNDg0YS0yYmRkLTQ2MzAtOGQ2Yy1iOGNiN2I0Mjk3ZDFcIiwgXCJncm91cFwiOiBcInVzZXJcIn0ifQ"
                                    ".eVygh9rRrwcPd46a9V9mhznhJh87Nt13LxwN17un_Us"
                                ),
                                "refreshToken": "cfb4d589-88b1-474b-8645-3c5a4f53c32c",
                                "userType": "sportsman",
                            },
                        },
                        "admin": {
                            "summary": "Refresh админа",
                            "value": {
                                "accessToken": (
                                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                    ".eyJleHAiOjE2OTkzNDExMjAsInN1YiI6IntcInVzZXJfaWRcIjogXCIxZTcyNDg0YS0yYmRkLTQ2MzAtOGQ2Yy1iOGNiN2I0Mjk3ZDFcIiwgXCJncm91cFwiOiBcInVzZXJcIn0ifQ"
                                    ".eVygh9rRrwcPd46a9V9mhznhJh87Nt13LxwN17un_Us"
                                ),
                                "refreshToken": "cfb4d589-88b1-474b-8645-3c5a4f53c32c",
                                "userType": "admin",
                            },
                        },
                    }
                }
            },
        },
        400: {
            "description": "`refreshToken` протух.",
            "content": {"application/json": {"example": {"detail": "refresh_token"}}},
        },
        404: {
            "description": "Сессия пользователя с таким `refreshToken` не найдена.",
            "content": {"application/json": {"example": {"detail": "refresh_token"}}},
        },
        422: {
            "description": "Ошибка валидации, `refreshToken` невалидный.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [{
                            "type": "string_type",
                            "loc": ["body", "refreshToken"],
                            "msg": "Input should be a valid string",
                            "input": 1,
                        }]
                    }
                }
            },
        },
    },
}


verify: Docs = {
    "summary": "Проверка валидности accessToken.",
    "description": """
    ```
    Request Body:
        accessToken - access токен авторизации.
                      (uuid)

    Auth:
        Этот запрос публичный.

    """,
    "responses": {
        200: {
            "description": "`accessToken` валидный.",
            "content": {"application/json": {"example": {}}},
        },
        401: {
            "description": "`accessToken` не был передан, или просросен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
    },
}


register: Docs = {
    "summary": "Регистрация пользователя",
    "description": """
    ```
    Request Body:
        email - почта.
                (string)

        password - пароль.
                   (string)(5 <= len <= 30)

    Auth:
        Этот запрос публичный.
    """,
    "responses": {
        201: {
            "description": "Успешная регистрация.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "c5300a69-ec99-473e-9df5-6b9c2db64eb9",
                        "email": "trainer@trainer.com",
                    }
                },
            },
        },
        409: {
            "description": "Пользователь с таким `email` уже существует.",
            "content": {
                "application/json": {"example": {"detail": "trainer/sportsman"}}
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


confirm_email: Docs = {
    "summary": "Подтверждение email.",
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
            "description": "Почта подтверждена.",
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


send_email: Docs = {
    "summary": "Отправка подтверждающего email.",
    "description": """
    ```
    Request Body:
        email - почта.
                (string)

        isTrainer - флаг пользователя.
                    (bool)

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
