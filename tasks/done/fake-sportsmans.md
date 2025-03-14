### ToDo
1. Теперь тренер может создавать фейковых спортсменов. 
   У фейков нет УЗ
2. Тренер может управлять фейком как настоящим.
3. Фейковых можно мерджить с настоящими.

### DoD
1. `POST   /api/trainer/local-sportsmans`       - добавление фейка по фио, где имя обязательно.
2. `PATCH  /api/trainer/local-sportsmans`       - обновление фио фейка
3. `DELETE /api/trainer/local-sportsmans`       - удаление фейка
4. `GET    /api/trainer/local-sportsmans`       - получение фейка/фейков
5. `POST   /api/trainer/local-sportsmans/merge` - мердж фейка с тру с сохранением истории.
6. Дока.
