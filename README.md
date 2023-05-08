# Это маленький rest сервис на django ninja

Сервис предоставляет небольшой функционал: можно зарегестрироваться, авторизоваться и добавлять в друзья других пользователей.

Сервис написан на django ninja, тесты на pytest (покрытие 95%).

**API** расписан в файлах `openapi.json` и `openapi.yaml`.

## Гайд по установке

1. склонировать репозиторий
2. `python3 -m venv venv` - создать виртуальное окружение
3. `source venv/bin/activate` - активировать виртуальное окружение
4. создать файл `.env` и вставить в него данные из `.env.sample` (конечно, предварительно отредактировав)
5. `pip3 install -r friendship/requirements.txt` - установить необходимые библиотеки.
6. `make build` - собрать докер образы приложения, админки и бд.
7. `docker exec -it web /bin/bash` - зайти в контейнер с приложением
8. `python3 manage.py makemigrations` - зафиксировать миграции
9. `python3 manage.py migrate` - применить миграции
10. `python3 manage.py createsuperuser` - создать админа (чтобы был) (далее следовать инструкциям джанги)
11. `exit` - выйти из контейнера.
12. перейти по `127.0.0.1:8000/api/v1/docs` - откроется страница с документацией openapi.
13. пользоваться сервисом


## Как менять код
1. выполнить шаги по установке
2. поменять код
3. поднять базу локально (см. параграф ниже).
4. `make lint` - проверить код линтером (flake8)
5. `make tests` - прогнать тесты (pytest)
6. `make build` - обновить докер образы.


## Как менять код без мучений
1. выполнить шаги по установке
2. в файле `docker-compose.yml` закомментировать образ приложения `web`.
3. у сервиса `db` раскомментировать порты
4. в настройках джанги `friendship/friendship/settings.py` у словаря 'default' списка `DATABASES` раскомментировать `'HOST': localhost'` и закомментировать `'HOST': os.environ.get('DB_HOST')`.
5. `make build` - собрать образ базы данных и её админки.
6. `make run` - запустить приложение.
7. `localhost:8080/` - адрес приложения, можно менять код и видеть результат мгновенно
8. `localhost:8081/` - адрес админки, там можно данные в бд смотреть.
9. когда сделали какой-то апдейт, то `make lint` и `make tests`.
10. обратно закомментировать и расскоментировать что закомментировали и раскомментировали.
11. `make build`
12. profit

## Как останавливать и запускать сервис
1. `make down` - остановить, если сервис запущен
2. `make up` - запустить, если сервис остановлен
3. `make build` - пересобрать docker образы. 

## Краткий функционал

`/api/v1/docs` - openapi документация. Далее описана часть функционала.

**User** в сервисе имеет поля uuid, username, password, date_created, is_staff.

#### функционал, связанный с юзерами
- `/api/v1/users/` - получить всех юзеров сервиса

#### функционал, связанный с авторизацией/регистрацией
- `/api/v1/register` - регистрация по username и password. Если ник не занят, то регистрируется новый юзер. Username может содержать только латинские буквы и цифры
- `/api/v1/login` - авторизация по username и password. Вовзращается токен, который живёт по умолчанию 10 минут. Его нужно отправлять в хедере (`'HTTP_AUTHORIZATION': 'Bearer token.example'`) (в сваггере можно авторизоваться и не мучаться с хедерами)
- `/api/v1/whoami` - возвращает username и uuid авторизованного пользователя.

#### функционал, связанный с дружбой (требуется авторизация)
- `/api/v1/friends/myfriends` - получить список своих друзей
- `/api/v1/friends/requests` - получить список исходящих и входящих заявок
- `/api/v1/friends/{user_id}/status` - получить статус дружбы с юзером по его user_id. Есть 4 статуса: **none**, **outgoing**, **incoming**, **friends**.
- `/api/v1/friends/{user_id}/add` - добавить юзера в друзья по его user_id. Если от этого юзера есть заявка в друзья, то статус дружбы с ним сменится с **incoming** на **friends**.
- `/api/v1/friends/{user_id}/remove` - удалить юзера из друзей / отменить заявку в друзья. Если юзер1 отправил заявку юзеру2, и юзер2 принял заявку, а потом юзер1 удалил юзера2 из друзей, то статус дружбы становится **none**. Если юзер1 отправил заявку юзеру2, и юзер2 принял заявку, а затем юзер2 передумал и удалил юзера1 из друзей, то заявка в друзья от юзера1 не удалится. Таким образом, накручивать подписчиков (входящие заявки) не получится.


## Пример использования:

Отправляем запрос: 

`post /api/v1/auth/register form={"username": "uniquename", "password": "qwerty1234"}`

получаем:

```
http 200
{
  "username": "uniquename",
  "id": "6ef18e97-1191-4ff8-8042-70f8400e43db"
}
```

зарегистрировали нового юзера. Если попытаемся зарегистрировать ещё одного юзера с таким именем, то получим следующее:
```
http 409
{
  "detail": "This username is already taken"
}
```

Теперь авторизуемся:

`post /api/v1/auth/login form={"username": "uniquename", "password": "qwerty1234"}`

получаем следующий респонс:

```
http 200
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNmVmMThlOTctMTE5MS00ZmY4LTgwNDItNzBmODQwMGU0M2RiIiwiZXhwIjoxNjgzNTc2NzM2LCJzdWIiOiJhY2Nlc3MifQ.dIYcpk5a7xElaF0UoA24SwSkPo7FIFd2GsSZZqYdVIw",
  "expires": "2023-05-08T20:12:16.780",
  "token_type": "bearer"
}
```

тут мы видим сам токен, дату и время окончания действия этого токена и его тип. Запоминаем этот токен, он нам пригодится. По умолчанию в приложении токены живут 5 минут, но это можно исправить в friendship/settings.py. 

Теперь отправляем все запросы со следующим хедером:
`'HTTP_AUTHORIZATION': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNmVmMThlOTctMTE5MS00ZmY4LTgwNDItNzBmODQwMGU0M2RiIiwiZXhwIjoxNjgzNTc2NzM2LCJzdWIiOiJhY2Nlc3MifQ.dIYcpk5a7xElaF0UoA24SwSkPo7FIFd2GsSZZqYdVIw'`

Если мы не укажем такой хедер, то не сможем обращаться к эндпоинтам, требущих авторизацию и будем получать следующий ответ:

```
http 401
{
  "detail": "Unauthorized"
}
```

Попробуем посмотреть своих друзей:
`get /api/v1/friends/myfriends`

получаем пустой список!:
```
http 200
[]
```

Добавим второго юзера:

`post /api/v1/auth/register form={"username": "user2", "password": "qwerty1234"}`
```
http 200
{
  "username": "user2",
  "id": "2d91d36d-57fc-4059-80bc-7beaa05b1cee"
}
```

и третьего:

`post /api/v1/auth/register form={"username": "user3", "password": "qwerty1234"}`

```
http 200
{
  "username": "user3",
  "id": "d6cd94c7-de65-4f42-b204-14354bc25429"
}
```

и четвёртого:

`post /api/v1/auth/register form={"username": "user4", "password": "qwerty1234"}`

```
http 200
{
  "username": "user4",
  "id": "b415a770-a420-40e3-9f3d-d3a7b7c434b8"
}
```

Добавим юзера2 в друзья!:

`post /api/v1/friends/2d91d36d-57fc-4059-80bc-7beaa05b1cee/add`

Получаем ответ:
```
http 200
{
  "detail": "ok"
}

```

И добавим юзера3 в друзья:

`post /api/v1/friends/d6cd94c7-de65-4f42-b204-14354bc25429/add`

```
http 200
{
  "detail": "ok"
}

```

Теперь авторизуемся как юзер2:

`post /api/v1/auth/login form={"username": "user2", "password": "qwerty1234"}`

получаем следующий респонс:

```
http 200
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMmQ5MWQzNmQtNTdmYy00MDU5LTgwYmMtN2JlYWEwNWIxY2VlIiwiZXhwIjoxNjgzNTc3MzgzLCJzdWIiOiJhY2Nlc3MifQ.OM0_EFrbSwbil7cD1j8aSE0w-qtm7xaB8olmppGGEWw",
  "expires": "2023-05-08T20:23:03.307",
  "token_type": "bearer"
}
```

Используем этот токен и отправляем запрос в друзья юзеру1:

`post /api/v1/friends/6ef18e97-1191-4ff8-8042-70f8400e43db/add`

Получаем ответ:
```
http 200
{
  "detail": "ok"
}
```

Теперь юзер1 и юзер2 друзья!

Авторизуемся за юзер4 и отправим запрос юзеру1:

`post /api/v1/friends/6ef18e97-1191-4ff8-8042-70f8400e43db/add`

Получаем:
```
http 200
{
  "detail": "ok"
}
```

Авторизуемся обратно за первого юзера и посмотрим на список его друзей:

`get /api/v1/friends/myfriends` (юзер1)

```
http 200
[
  {
    "username": "user2",
    "id": "2d91d36d-57fc-4059-80bc-7beaa05b1cee"
  }
]
```

Юзер2 появился в списке друзей!

Посмотрим на заявки в друзья юзера1:

`get /api/v1/friends/requests` (юзер1)

```
http 200
{
  "incoming": [
    {
      "username": "user4",
      "id": "b415a770-a420-40e3-9f3d-d3a7b7c434b8"
    }
  ],
  "outgoing": [
    {
      "username": "user3",
      "id": "d6cd94c7-de65-4f42-b204-14354bc25429"
    }
  ]
}
```

Действительно, мы отправили заявку юзеру1 за юзера4 и юзеру3 за юзера1. Юзера2 здесь нет, т.к. он уже в друзьях.

Можем проверить статус дружбы со всеми пользователями:

user2:

`get /api/v1/friends/2d91d36d-57fc-4059-80bc-7beaa05b1cee/status`

```
http 200
{
  "status": "friends"
}
```

user3:

`get /api/v1/friends/d6cd94c7-de65-4f42-b204-14354bc25429/status`

```
http 200
{
  "status": "outgoing"
}
```

user4:

`get /api/v1/friends/b415a770-a420-40e3-9f3d-d3a7b7c434b8/status`

```
http 200
{
  "status": "incoming"
}
```

uniquename:

`get /api/v1/friends/6ef18e97-1191-4ff8-8042-70f8400e43db/status`

```
http 200
{
  "status": "none"
}
```

Заявку отправить самому себе не получится. вернётся ошибка.

Удалим юзера2 из друзей. Так как юзер1 первым отправил заявку, то заявка юзера2 удалится (типа чтобы не накручивать подписчиков)

`post /api/v1/friends/2d91d36d-57fc-4059-80bc-7beaa05b1cee/remove`

```
http 200
{
  "detail": "ok"
}
```

Проверим статус дружбы с юзером2:

`get /api/v1/friends/2d91d36d-57fc-4059-80bc-7beaa05b1cee/status`

```
http 200
{
  "status": "none"
}
```

Вот такой небольшой функционал предоставляет данный сервис. Все эндпоинты описаны в openapi.json/openapi.yaml и по урлу `/api/v1/docs`.
