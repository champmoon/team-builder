### ToDo
1. Спортсмен никак не может управлять статусом тренировки.
2. У тренировки убираются статусы: Запланированна -> Активна -> ...
3. Тренер проставляет был/не был спортсмен на тренировке.
4. У тренировки появляюстя поле цены.
5. Тренер проставляет заплатил/не заплатил спортсмен за тренировку.


### DoD
1. В тренировках во все запросах  `/api/trainer/workouts/...`:
   * убирается поле `stressQuestionnaireTime`
   * убирается поле `status`
   * добавляется поле `price`
2. Вместо статуса тренировки появляется поле `isAttend=true/false`. 
   Поле будет показываться только в запросе получения 
   статистики спортсменов по этой тренировки и в запросах измнения новый полей.
3. Добавляется поле `isPaid=true/false`, по аналогии.
4. Убираются запросы:
   1. `PATCH /api/trainer/workouts/start`
   2. `PATCH /api/trainer/workouts/sportsmans/start`
   3. `PATCH /api/trainer/workouts/compelete`
   4. `PATCH /api/trainer/workouts/sportsmans/compelete`
   5. `PATCH /api/trainer/workouts/cancel`
   6. `PATCH /api/trainer/workouts/sportsmans/cancel`
   7. `PATCH /api/trainer/workouts/statuses`
5. Добавляются запросы:
   1. `PATCH /api/trainer/workouts/attend/yes` - по массиву айдишников спортиков тренер проставляет посещаемость. Базово `isAttend=false`.
   2. `PATCH /api/trainer/workouts/attend/no` - по массиву айдишников спортиков тренер проставляет отсутствие. Если случайно тренер выбрал не того, может поменять.
   3. `PATCH /api/trainer/workouts/paid/yes` - по аналогии
   4. `PATCH /api/trainer/workouts/paid/no` - по аналогии
   5. `GET /api/trainer/workouts/stats` - по id трени статистику.
   включает всю инфу трени и новый полей. 
6. Обновить доку.
