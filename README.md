# m_olya_nail_backend
___
____
## Запуск:
:one: . Создается БД PostgreSQL.

:two: . На одном уровне с файлом dist.env создается файл .env с необходимыми данными:

- `SECRET_KEY` - `SECRET_KEY` для `setting.SECRET_KEY` 


- `DB_NAME` - Название базы данных
   

- `PG_USER` - Логин пользователя базы данных с правами управления базой данных `DB_NAME`.
   

- `PG_PASSWORD` - Пароль пользователя `DB_USER`.
   

- `DB_HOST` - Адрес сервера, на котором расположена база данных  `DB_NAME`.
   

- `DB_PORT` - Порт, через который устанавливается соединение с базой данных `DB_NAME`.
  

- `DEBUG` - принимает одно из значений - `True` или `False`  
  

- `ADMIN_ADDRESS` - принимает любое значение типа SLUG. Используется для построения 
   URL к сайту администрирования. 
  

- `REFERRAL_BONUS` - целое число. 
  

- `REFERRAL_FIXED_BONUS` - целое число. 


- `FREE_BONUS` - целое число. 


- `FREE_CODE` - строка.

___

:three: . <code>pip install -r requirements.txt</code>

___
:four: . <code>python manage.py makemigrations</code>
   
   <code>python manage.py migrate</code>
___

:five: . Создаем пользователя для доступа в админке:
   <code>python manage.py createsuperuser</code>
___

:six: . <code>python manage.py runserver</code>