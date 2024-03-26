# Импорт базового класса моделей и движка базы данных
from db import Base, engine

# Импортируем нужные нам элементы для создания таблиц
from sqlalchemy import Column, Integer, String

# Определение модели User для хранения информации о пользователях
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=False)

# Определение модели Technique для хранения информации о техниках из Naruto
class Technique(Base):
    __tablename__ = 'techniques_Naruto'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    episode = Column(String, nullable=False)
    element = Column(String)
    type_tech = Column(String)
    rank = Column(String)
    counter = Column(Integer, default=0)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
