from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from app.models.task import Task

from app.backend import *

#В модуле user.py создайте модель User, наследованную от ранее написанного Base со следующими атрибутами:
    # __tablename__ = 'users'
    # id - целое число, первичный ключ, с индексом.
    # username - строка.
    # firstname - строка.
    # lastname - строка.
    # age - целое число.
    # slug - строка, уникальная, с индексом.
    # tasks - объект связи с таблицей с таблицей Task, где back_populates='user'.


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="user") # связали 'Task' с 'user'


from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))
print(CreateTable(User.__table__))
