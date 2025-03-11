### ToDo
1. Добавить поле `rememberMe` при авторизации


### DoD
1. В запрос `/api/auth/login` добавить поле `rememberMe`, которое по дефолту `False`
   Если `False`, то `refreshToken` будет жить 1 день.
   Если `True`. то `refreshToken` живет 1 месяц.
2. Обновить доку.
