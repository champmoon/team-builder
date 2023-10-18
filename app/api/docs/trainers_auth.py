from .base_docs import Docs

register: Docs = {
    "summary": "Регистрация тренера",
    "description": """
    ```
    Request Body:
        email - почта тренера.(string)(unique=True)
        password - пароль тренера.(string)
        name - имя тренера.(string)
    
    Auth:
        Этот запрос публичный.
    """,
    "responses": {
        201: {
            "description": "Успешная регистрация нового тренера.",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
                        "name": "string",
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


login: Docs = {
    "summary": "Авторизация тренера",
    "description": """
    ```
    Request Body:
        email - почта тренера.(string)(unique=True)
        password - пароль тренера.(string)
        name - имя тренера.(string)

    Auth:
        Этот запрос публичный.
    """,
    "responses": {
        200: {
            "description": (
                "Успешная авторизация нового тренера, получение пары `jwt"
                " access/refresh токенов`."
            ),
            "content": {
                "application/json": {
                    "example": {
                        "accessToken": (
                            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                            ".eyJleHAiOjE2OTkzNDExMjAsInN1YiI6IntcInVzZXJfaWRcIjogXCIxZTcyNDg0YS0yYmRkLTQ2MzAtOGQ2Yy1iOGNiN2I0Mjk3ZDFcIiwgXCJncm91cFwiOiBcInVzZXJcIn0ifQ"
                            ".eVygh9rRrwcPd46a9V9mhznhJh87Nt13LxwN17un_Us"
                        ),
                        "refreshToken": "cfb4d589-88b1-474b-8645-3c5a4f53c32c",
                        "userType": "trainer",
                    }
                }
            },
        },
        404: {
            "description": "Тренер с таким `email` не найден.",
            "content": {
                "application/json": {
                    "example": {"detail": "Trainer with email {email} not found"}
                }
            },
        },
        409: {
            "description": "Неверный `password`.",
            "content": {
                "application/json": {"example": {"detail": "Trainer password didnt match"}}
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
            "description": "Пользователь временно заблокирован.",
            "content": {
                "application/json": {
                    "example": {"detail": "User is locked - email/password"}
                }
            },
        },
    },
}

logout: Docs = {
    "summary": "Выход с аккаунта тренера",
    "description": """
    ```
    Request Body:
        refreshToken - рефреш токен авторизации.(uuid)
    
    Auth:
        Этот запрос требует авторизации типа пользователя - тренера.

    P.S.:
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
    },
}

refresh: Docs = {
    "summary": "Получение новой пары токенов с помощью refreshToken.",
    "description": """
    ```
    Request Body:
        refreshToken - refresh токен авторизации.(string)

    Auth:
        Этот запрос публичный.
    """,
    "responses": {
        201: {
            "description": "`refreshToken` валидный. Получена новая пара токенов.",
            "content": {
                "application/json": {
                    "example": {
                        "accessToken": (
                            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                            ".eyJleHAiOjE2OTkzNDExMjAsInN1YiI6IntcInVzZXJfaWRcIjogXCIxZTcyNDg0YS0yYmRkLTQ2MzAtOGQ2Yy1iOGNiN2I0Mjk3ZDFcIiwgXCJncm91cFwiOiBcInVzZXJcIn0ifQ"
                            ".eVygh9rRrwcPd46a9V9mhznhJh87Nt13LxwN17un_Us"
                        ),
                        "refreshToken": "0b31b17f-2513-4dcc-899d-debfca437cdc",
                        "tokenType": "Bearer",
                    }
                }
            },
        },
        400: {
            "description": "Рефреш токен протух.",
            "content": {
                "application/json": {"example": {"detail": "Refresh token expired"}}
            },
        },
        404: {
            "description": "Сессия пользователя с таким рефреш токеном не найдена.",
            "content": {
                "application/json": {"example": {"detail": "Refresh token not found"}}
            },
        },
        422: {
            "description": "Ошибка валидации, какой-то параметр был передан неверно.",
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
        Этот запрос требует авторизации любой групп пользователей.

    P.S.:
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
