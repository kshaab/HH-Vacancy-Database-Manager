# Job search with database connection 

### Программа получения данных с сайта hh.ru, загрузке их в базу данных и получения информации через запросы в базу данных.

### Проект завершен.

## Содержание 

- [Использование](#использование)
- [Разработка](#разработка)
- [Зависимости](#зависимости)
- [Автор](#автор)


## Использование
Клонируйте репозиторий: 
```bash
git clone https://github.com/kshaab/Coursework_3
cd crswrk_3
```
Установите зависимости и активируйте виртуальное окружение: 
poetry install
poetry shell

Запустите файл: 
python src/main.py


## Разработка

## Функциональность 

### base_hh_api
- ### `class BaseClassAPI(ABC)` 
Базовый класс для работы с API.

### base_dbmanager 
- ### `class BaseDBManager(ABC)`
Базовый класс для работы с БД.

### hh_api
- ### `class HeadHunterAPI(BaseClassAPI)`
Класс для работы с API hh.ru.

### utils
- ### `create_database()` 
Функция создания базы данных и таблиц для сохранения данных об организациях и вакансиях.
- ### `save_data_to_database`
Функция сохранения данных о компаниях и вакансиях в базу данных.

### dbmanager 
- ### `class DBManager(BaseDBManager)`
Класс для работы с базой данных PostgreSQL.

### interaction_function.py
- ### `user_interaction()`
Функция взаимодействия с пользователем.

### Main
- ### `main()`
Объединяет работу модулей в единую программу.


## Зависимости
Управление зависимостями осуществляется через Poetry (pyproject.toml).


## Автор
[Ксения](https://github.com/kshaab)