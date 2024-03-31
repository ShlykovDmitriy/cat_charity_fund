

# **Благотворительный фонд для поддержки котиков.** 

## Описание
___
Фонд для сбора пожертвований на проекты для помощи хвостатым.
Пожертвования распределяются по проектом начиная с первого.
___
## Технологии
___
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) 
![BeautifulSoup](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=for-the-badge&logo=sqlalchemy&logoColor=white)



___
## Установка и запуск
___
1. Склонируйте репозиторий на свой компьютер:
```bash 
git clone git@github.com:ShlykovDmitriy/cat_charity_fund.git
```

2. Создайте виртуальное окружение в корне проекта и активируйте его :

```bash 
python -m venv venv
source venv/bin/activate
```

3. Установите зависимости :


```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
``` 

4. Создать файл .env с переменными
```bash
APP_TITLE=<Название>
DATABASE_URL=<База данных>
SECRET_KEY=<Секретный ключ>
``` 

5. Примените миграции:
```bash
alembic upgrade head
```


6. Запустите программу:
```bash
uvicorn app.main:app
```

7. Ознакомтесь по адресу
```bash
http://127.0.0.1:8000/
```




___
### Автор
___
[Шлыков Дмитрий](https://github.com/ShlykovDmitriy)