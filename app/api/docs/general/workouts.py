from ..base_docs import Docs

get_workouts: Docs = {
    "summary": "Получение всех тренировок",
    "description": """
    ```
    Query params:
        id - ID тренировки.(uuid|null)(default=null)

        offset - отступ.(int)(default=0)

        limit - лимит.(int)(default=100)

        start_date - дата начала.(date)(default=null)

        end_date - дата окончания.(date)(default=null)

    Auth:
        Этот запрос доступен тренерам и спортсменам.

    P.S:
        Ответ зависит от типа пользователя.
        Если указать id, присылается одна тренировка,
        иначе список

    """,
    "responses": {
        200: {
            "description": "Полученные тренировки",
            "content": {
                "application/json": {
                    "examples": {
                        "trainer": {
                            "summary": "Тренировки тренера",
                            "value": [{
                                "id": "710e45d6-3cdc-4cfd-a952-460f82b0c3a2",
                                "repeatId": "468288a3-c5ef-43e5-a3f2-23b631bd325f",
                                "name": "string",
                                "estimatedTime": 0,
                                "restTime": 0,
                                "price": 123,
                                "date": "2026-03-21T15:55:44.459000",
                                "createdAt": "2025-03-21T15:55:19.236679",
                                "comment": "string",
                                "goal": "string",
                                "exercises": [{
                                    "id": "72a2dbbe-f661-81ca-89a06a174cdd",
                                    "type": {
                                        "type": 4,
                                        "description": "Отжимания",
                                        "isBasic": True,
                                    },
                                    "reps": 2,
                                    "sets": 2,
                                    "rest": 2,
                                    "order": 1,
                                }],
                                "workoutType": "Командная",
                                "teamId": "942a0e54-a233-4ce9-8090-2d9363de6fea",
                            }],
                        },
                        "sportsman": {
                            "summary": "Тренировки спортсмена",
                            "value": [{
                                "id": "710e45d6-3cdc-4cfd-a952-460f82b0c3a2",
                                "repeatId": "468288a3-c5ef-43e5-a3f2-23b631bd325f",
                                "name": "string",
                                "estimatedTime": 0,
                                "restTime": 0,
                                "price": 123,
                                "date": "2026-03-21T15:55:44.459000",
                                "createdAt": "2025-03-21T15:55:19.236679",
                                "comment": "string",
                                "goal": "string",
                                "exercises": [{
                                    "id": "72a2dbbe-f661-43fd-89a06a174cdd",
                                    "type": {
                                        "type": 4,
                                        "description": "Отжимания",
                                        "isBasic": True,
                                    },
                                    "reps": 2,
                                    "sets": 2,
                                    "rest": 2,
                                    "order": 1,
                                }],
                                "sportsmanId": "3fa85f64-5717-b3fc-2c963f66afa6",
                                "workoutType": "Командная",
                                "teamId": "942a0e54-a233-4ce9-8090-2d9363de6fea",
                            }],
                        },
                    }
                },
            },
        },
        401: {
            "description": "Пользователь не авторизан, или `accessToken` просрочен.",
            "content": {"application/json": {"example": {"detail": "Unauthorized"}}},
        },
        403: {
            "description": "Пользователь не является тренером/спортсменом.",
            "content": {"application/json": {"example": {"detail": "Forbidden"}}},
        },
        404: {
            "description": "Тренировка не найдена.(id)",
            "content": {"application/json": {"example": {"detail": "workout"}}},
        },
    },
}
