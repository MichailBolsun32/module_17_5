from fastapi import FastAPI
from app.routers import task, user

#В файле main.py создайте сущность FastAPI(),
app = FastAPI()

# напишите один маршрут для неё - '/',
# по которому функция возвращает словарь - {"message": "Welcome to Taskmanager"}.
@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to Taskmanager"}

# Импортируйте объекты APIRouter и подключите к ранее созданному приложению FastAPI,
# объединив все маршруты в одно приложение.
app.include_router(user.router)
app.include_router(task.router)
