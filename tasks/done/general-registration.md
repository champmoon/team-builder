### ToDo
1. Объединить регистрацию спортсмена и тренера
2. Убрать ФИО из регистрации
3. Спортсмены могут регать себя сами


### DoD
1. Объединение запросов:
   1. `/api/trainer/email`, `/api/sportsman/email` -> `/api/auth/email`
   2. `/api/trainer/email/confirm`, `/api/sportsman/email/confirm` -> `/api/auth/email/confirm`
   3. `/api/trainer/register`, `/api/sportsman/register` -> `/api/auth/register`
2. В запросе `/api/trainer/email` добавляется поле `is_trainer=true/false`
3. В запросе `/api/trainer/register` больше нет полей `first_name`, `middle_name`, `last_name`
4. Тренер/спортмен могут регистрировать себя сами.
5. Обновить доку.
