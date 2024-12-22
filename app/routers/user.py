from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models.user import User, Task
from app.schemas import CreateUser, UpdateUser, CreateTask, UpdateTask

from sqlalchemy import insert, select, update, delete
from slugify import slugify

#В модуле user.py напишите APIRouter с префиксом '/user' и тегом 'user',
router = APIRouter(prefix='/user', tags=["user"])

# Создайте новый маршрут get "/user_id/tasks"
# и функцию tasks_by_user_id.
# Логика этой функции должна заключатся в возврате всех Task конкретного User по id.
@router.get("/user_id/tasks")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):

    user_ = db.scalar(select(User).where(User.id == user_id))
    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    subtasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return subtasks

#     Функция all_users ('/'):
#     Должна возвращать список всех пользователей из БД. Используйте scalars, select и all
@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users_ = db.scalars(select(User)).all()
    return users_

# Функция user_by_id ('/user_id'):
# Для извлечения записи используйте ранее импортированную функцию select.
#     Дополнительно принимает user_id.
#     Выбирает одного пользователя из БД.
#     Если пользователь не None, то возвращает его.
#     В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"
@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):

    user_ = db.scalar(select(User).where(User.id == user_id))
    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    return user_

# Функция craete_user ('/create'):
# Для добавления используйте ранее импортированную функцию insert.
#     Дополнительно принимает модель CreateUser.
#     Подставляет в таблицу User запись значениями указанными в CreateUser.
#     В конце возвращает словарь {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
#     Обработку исключения существующего пользователя по user_id или username можете сделать по желанию.
@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], createUser: CreateUser):

    user_ = db.scalar(select(User).where(User.username == createUser.username))
    if user_ is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is already a user with that name'
        )

    db.execute(insert(User).values(username=createUser.username,
                                       firstname=createUser.firstname,
                                       lastname=createUser.lastname,
                                       age=createUser.age,
                                       slug=slugify(createUser.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

# Функция update_user ('/update'):
# Для обновления используйте ранее импортированную функцию update.
#     Дополнительно принимает модель UpdateUser и user_id.
#     Если находит пользователя с user_id, то заменяет эту запись значениям из модели UpdateUser.
#     Далее возвращает словарь {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
#     В противном случае выбрасывает исключение с кодом 404 и описанием "User was not found"
@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, updateUser: UpdateUser):

    user_ = db.scalar(select(User).where(User.id == user_id))
    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    db.execute(update(User).where(User.id == user_id).values(
                                   firstname=updateUser.firstname,
                                   lastname=updateUser.lastname,
                                   age=updateUser.age))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }



#  Дополните функцию delete_user так,
#  чтобы вместе с пользователем удалялись все записи связанные с ним.
@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):

    user_ = db.scalar(select(User).where(User.id == user_id))
    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    db.execute(delete(Task).where(Task.user_id == user_id))
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }