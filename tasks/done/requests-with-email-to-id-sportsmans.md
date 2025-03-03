### ToDo
1. Так как тепень есть фиктивные спортсмены, 
   все запросы со спортсменами должны быть теперь по `id`, а не по `email`

### DoD
1. Следующие запросы теперь работают по `id` спортсмена:
   1. `POST` `/api/trainer/groups`
   2. `POST` `/api/trainer/groups/add`
   3. `POST` `/api/trainer/groups/adds`
   4. `POST` `/api/trainer/groups/kick`
   5. `POST` `/api/trainer/groups/kicks`
   6. `GET`  `/api/trainer/workouts/sportsman`
   7. `POST` `/api/trainer/workouts/individual`
   8. `POST` `/api/trainer/workouts/individual/repeat`
2. Обновил доку на эти запросы.
