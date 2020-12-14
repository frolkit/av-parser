# [av-parser](https://avito.frolkit.ru/)
Это тестовое задание для стажировки в avito.ru. Этот проект позволяет отслеживать заданные поисковые запросы формата: "поисковой запрос", "локация".
Проект раз в час отслеживает и сохраняет колличество объявлений по запросам, а так может вывести последние 5 объявлений.

Стек: Django, DRF, Python, Celery, Docker, Unittest, PostgreSQL, Nginx.

Проект доступен: https://avito.frolkit.ru/

Документация: https://avito.frolkit.ru/redoc/

## Инструкция по развёртыванию.
1. Создайте отдельную папку для проекта. Все дальнейшие действия выполняйте из неё.

2. Скопируйте себе файл docker-compose.yaml

3. Создайте и заполните файл .env
```
DEBUG=False
SECRET_KEY=Получите ключ
AVITO_AUTH_KEY=Получите ключ
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgresql
POSTGRES_USER=postgresql
POSTGRES_PASSWORD=postgresql
DB_HOST=db
DB_PORT=5432
```

4. Запустите контейнеры
```
docker-compose up -d
```

5. Сделайте миграции.
```
docker-compose exec web python manage.py migrate
```

6. Соберите статику для работы документации.
```
docker-compose exec web python manage.py collectstatic
```

7. Проект доступен по 127.0.0.1:80


## Запуск тестирования.

1. Тестирование можно запустить только в среде разработки. В .env включите DEBUG мод.
```
DEBUG=True
SECRET_KEY=Получите ключ
AVITO_AUTH_KEY=Получите ключ
```

2. Запустите тесты
```
python manage.py test
```

## Получение SECRET_KEY и AVITO_AUTH_KEY.

1. SECRET_KEY можно получить по [ссылке](https://djecrety.ir/).

2. AVITO_AUTH_KEY.
```
Тут сложно..
```
