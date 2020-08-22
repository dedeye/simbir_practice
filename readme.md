# Сервис Goods

## Описание
Сервис объявлений любого типа

## swagger
http://localhost:8000/swagger/

## api

### localhost:8000/api/v1/advert GET
возвращает список объявлений в кратком предствалении

### localhost:8000/api/v1/advert GET
добавление нового объявления

### localhost:8000/api/v1/advert/{id} GET|PUT|PATCH|DELET
получение/изменение/удаление объявления по id


### localhost:8000/api/v1/advert/filter/ GET
получение списка объявлений в кратком представлении 
способы фильтрации: по списку тэгов, по дате создания, по цене
способы сортировки: по дате создания, по цене

### localhost:8000/api/v1/advert/{id}/brief/ GET
получение объявления в кратком виде по id

### localhost:8000/api/v1/advert/all_tags/
получение списка всех доступных тэгов

### localhost:8000/api/v1/advert/{id}/img POST
добавление изображения к объявлению c определенным id

### localhost:8000/api/v1/img/{id} GET DELETE
получение/удаление изображения по id



# Сервис User_auth

## Описание 
Сервис авторизации на основе JWT

## swagger 
http://localhost:8000/swagger/
в поле AUTHORIZATION перед JWT следует указывать `Bearer`

## Применение миграций
`docker-compose exec sh -c "cd user_auth && alembic upgrade head"`

### localhost:8080/api/v1/register/
регистрирует нового пользователя с ролью user

### localhost:8080/api/v1/login/
Вход в систему: генерирует JWT-Pair для пользователя

### localhost:8080/api/v1/validate/
Проверяет корректность JWT, возвращает payload

### localhost:8080/api/v1/refresh/
Обновление JWT-Pair с помощью refresh token

### localhost:8080/api/v1/logout/
Выход из системы: инвалидация JWT-Pair
