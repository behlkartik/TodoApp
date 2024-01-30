from fastapi import APIRouter, Depends, HTTPException, status, Path
import typing as t
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Todos
from routers.auth import get_current_user

app = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


db_dependency = t.Annotated[Session, Depends(get_db)]
user_dependency = t.Annotated[t.Dict, Depends(get_current_user)]


@app.get("/todos", status_code=status.HTTP_200_OK)
async def get_all(user: user_dependency, db: db_dependency):
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action!!!")
    return db.query(Todos).all()


@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_one(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action!!!")
    existing_todo = db.query(Todos).filter(Todos.id == todo_id).one_or_none()
    if not existing_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found!!!")
    db.delete(existing_todo)
    db.commit()
