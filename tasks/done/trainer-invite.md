### ToDo
1. Тренер может пригласить спортсмена по почте, так и сформировать ссылку для вступления в команду. Также тренер может удалить из команды.
2. Спортсмен переходит по ссылке и добавляется в команду. Также спортсмен может уйти из команды


### DoD
1. `POST /api/trainer/sportman/invite` - приглашение спортика по email, необязательный параметр `local_sportsman_id`, ему на почту прилетает ссылка для вступления в команду. 
2. `POST /api/trainer/team/invite` - создание ссылки приглашение в команду.
3. `POST /api/trainer/team/kick` - выгнать спортсменов по их `email`.
4. `POST /api/sportsman/team/join` - спортсмен вступает в команду.
5. `POST /api/sportsman/team/out` - спортсмен уходит из команды.
