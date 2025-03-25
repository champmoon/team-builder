### ToDo
1. Тренер теперь может сам регистрироваться.


### DoD
1. Алгоритм регистрации тренера:
   1. Тренер делает запрос на `/api/trainer/email` БЕЗ токена авторизации, \
   при этом поля `firstName`, `middleName`, `lastName`, `teamName`, `sportType` исчезают:
   ```bash
   {
      "email": "user@example.com"
   }
   ```
   на почту ему приходит ссылка на подтверждение почты, \
   если `swagger` в режиме `DEBUG=True`, то ответ придет еще и в респонсе:
   ```bash
   {
      "uri": "https://tbuilder.pro/register/confirm_token=7a32cb4c-ed9b-41c3-a8e1-7a95ab074e94",
      "expire": 300
   }
   ```
   параметр `expire` остался тем же.

   2. Этап с `/api/trainer/email/confirm` остается прежним.
   
   3. При запросе `/api/trainer/register` тело запроса теперь выглядит так:
   ```bash
   {
      "email": "user@example.com",
      "firstName": "string",
      "middleName": "string",
      "lastName": "string",
      "password": "string"
   }
   ```
   то есть исчезли поля `teamName` и `sportType`. \
   поля ответа не изменились.
