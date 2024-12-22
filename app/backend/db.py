# В модуле db.py:

#     Импортируйте все необходимые функции и классы , создайте движок указав пусть в
#     БД - 'sqlite:///taskmanager.db' и локальную сессию (по аналогии с видео лекцией).
#     Создайте базовый класс Base для других моделей, наследуясь от DeclarativeBase.


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String

engine = create_engine("sqlite:///taskmanager.db", echo=True)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass