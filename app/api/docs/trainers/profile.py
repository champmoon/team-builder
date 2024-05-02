from ..base_docs import Docs

get_profile: Docs = {
    "summary": "Получение профиля тренера",
    "description": """
    ```
    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получен профиль тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
                        "firstName?": "string",
                        "middle_name?": "string",
                        "last_name?": "string",
                        "avatar_uri?": "http://localhost/kjf;sdflksdf;lsdjf;s/",
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


update_profile: Docs = {
    "summary": "Обновление профиля тренера",
    "description": """
    ```
    Request Body:
        first_name - имя тренера.
               (string)(required=False)

        middle_name - фамилия тренера.
               (string)(required=False)

        last_name - отчество тренера.
               (string)(required=False)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Получен обновлённый профиль тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
                        "firstName?": "string",
                        "middle_name?": "string",
                        "last_name?": "string",
                        "avatar_uri?": "http://localhost/kjf;sdflksdf;lsdjf;s/",
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
            "description": "Ошибка валидации, `name` невалидный.",
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


upload_avatar: Docs = {
    "summary": "Загрузка аватара тренера",
    "description": """
    ```
    Request Body:
        avatar - аватар тренера.(file)

    Auth:
        Этот запрос доступен только тренерам.
    """,
    "responses": {
        200: {
            "description": "Обновлённый профиль тренера",
            "content": {
                "application/json": {
                    "example": {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "email": "string",
                        "firstName?": "string",
                        "middle_name?": "string",
                        "last_name?": "string",
                        "avatar_uri": "http://localhost/kjf;sdflksdf;lsdjf;s/",
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
            "description": "Ошибка валидации, что то не так.",
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
