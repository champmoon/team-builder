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
                        "detail": [
                            {
                                "type": "string_type",
                                "loc": ["body", "refreshToken"],
                                "msg": "Input should be a valid string",
                                "input": 1,
                            }
                        ]
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
    Auth:
        Этот запрос требует авторизации любого типа пользователей.

    P.S.
        accessToken передаётся в хедере - Authorization: Bearer <accessToken>,
        как и во всех запросах, требующих авторизации.
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
