from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models.user import User, Task
from app.schemas import CreateUser, UpdateUser, CreateTask, UpdateTask

from sqlalchemy import insert, select, update, delete
from slugify import slugify

#В модуле task.py напишите APIRouter с префиксом '/task' и тегом 'task',
router = APIRouter(prefix='/task', tags=["task"])

#  Функция all_tasks ('/') - идентично all_users.
@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    task_ = db.scalars(select(Task)).all()
    return task_

# Функция task_by_id ('/task_id') - идентично user_by_id (тоже по id)
@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task_ = db.scalar(select(Task).where(Task.id == task_id))
    if task_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )

    return task_

#  Функция craete_task ('/create'):
#     Дополнительно принимает модель CreateTask и user_id.
#     Подставляет в таблицу Task запись значениями указанными в CreateUser и user_id,
#           если пользователь найден. Т.е. при создании записи Task вам необходимо связать её с
#           конкретным пользователем User.
#     В конце возвращает словарь {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
#     В случае отсутствия пользователя выбрасывает исключение с кодом 404 и описанием "User was not found"
@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], user_id: int, createTask: CreateTask):
    user_ = db.scalar(select(User).where(User.id == user_id))

    if user_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    db.execute(insert(Task).values(title=createTask.title,
                                   content=createTask.content,
                                   priority=createTask.priority,
                                   user_id=user_id,
                                   slug=slugify(createTask.title)))
    db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


#  Функция update_task ('/update') - идентично update_user.
@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, updateTask: UpdateTask):

    task_ = db.scalar(select(Task).where(Task.id == task_id))
    if task_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )

    db.execute(update(Task).where(Task.id == task_id).values(
                                                    itle=updateTask.title,
                                                    content=updateTask.content,
                                                    priority=updateTask.priority))

    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


# Функция delete_task ('/delete') - идентично delete_user.
@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):

    task_ = db.scalar(select(User).where(Task.id == task_id))
    if task_ is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }