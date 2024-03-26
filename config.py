import os

# Переменная содержит абсолютный путь к текущему каталогу
basedir = os.path.abspath(os.path.dirname(__file__))

TOKEN = ''

# Подключение к БД, а также создается путь к файлу БД
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
