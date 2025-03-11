### ToDo
1. Добавить функционал сброса(восстановление) пароля.


### DoD
1. Запрос `/api/auth/password/send` принимает в себя `email`,
   отдает:
   если `DEBUG=False`, то только `expire`,
   если `DEBUG=True`, то `expire` и `uri`.
   В урле содержится `confirm_token`, который надо будет подтвердить.
2. Запрос `/api/auth/password/confirm`, который принимает в себя `confirm_token`.
3. Запрос `/api/auth/password`, который принимает поле `password` и обвноляет его.
4. Документация.
