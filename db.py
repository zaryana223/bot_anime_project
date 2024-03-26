from config import SQLALCHEMY_DATABASE_URI

# Импорт необходимых классов и функций из библиотеки SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Создание сессии для взаим-я с БД
db_session = scoped_session(sessionmaker(bind=engine))

# Создание базового класса моделей
Base = declarative_base()

# Кидает запросы к БД через сессию 
Base.query = db_session.query_property()
