from fastapi import APIRouter, Depends, HTTPException, status, Path
import typing as t
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Todos
from schemas import TodoRequest
from routers.auth import get_current_user

app = APIRouter(
    prefix="/todos",
    tags=["todos"]
)


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


db_dependency = t.Annotated[Session, Depends(get_db)]
user_dependency = t.Annotated[t.Dict, Depends(get_current_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency, user: user_dependency):
    return db.query(Todos).filter(Todos.owner_id == user["id"]).all()


@app.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_by_id(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):
    existing_todo = db.query(Todos).filter(Todos.owner_id == user["id"]).filter(Todos.id == todo_id).one_or_none()
    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"To-do with id {todo_id} not found!!!")
    return existing_todo


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_one(create_todo: TodoRequest, user: user_dependency, db: t.Annotated[Session, Depends(get_db)]):
    new_todo = Todos(**create_todo.model_dump(), owner_id=user["id"])
    db.add(new_todo)
    db.commit()


@app.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_one(db: t.Annotated[Session, Depends(get_db)],
                     user: user_dependency,
                     update_todo_request: TodoRequest,
                     todo_id: int = Path(gt=0)):
    existing_todo = db.query(Todos).filter(Todos.owner_id == user["id"]).filter(Todos.id == todo_id).one_or_none()
    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"To-do with id {todo_id} not found!!!")
    existing_todo.title = update_todo_request.title
    existing_todo.description = update_todo_request.description
    existing_todo.priority = update_todo_request.priority
    existing_todo.complete = update_todo_request.complete
    db.add(existing_todo)
    db.commit()


@app.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one(db: t.Annotated[Session, Depends(get_db)], user: user_dependency, todo_id: int = Path(gt=0)):
    existing_todo = db.query(Todos).filter(Todos.owner_id == user["id"]).filter(Todos.id == todo_id).one_or_none()
    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"To-do with id {todo_id} not found!!!")
    db.delete(existing_todo)
    db.commit()
