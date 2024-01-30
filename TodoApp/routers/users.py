from fastapi import APIRouter, Depends, HTTPException, status, Path
import typing as t
from database import SessionLocal
from sqlalchemy.orm import Session
from routers.auth import get_current_user
from passlib.context import CryptContext
from models import Users
from schemas import UpdateUserPasswordRequest, UpdateUserDetailsRequest

app = APIRouter(
    prefix="/users",
    tags=["users"]
)


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


db_dependency = t.Annotated[Session, Depends(get_db)]
user_dependency = t.Annotated[t.Dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    return db.query(Users).filter(Users.id == user["id"]).one_or_none()


@app.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, update_user_request: UpdateUserPasswordRequest):
    existing_user: Users = db.query(Users).filter(Users.id == user["id"]).one_or_none()
    if not bcrypt_context.verify(update_user_request.old_password, existing_user.hashed_pwd):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    existing_user.hashed_pwd = bcrypt_context.hash(update_user_request.new_password)
    db.add(existing_user)
    db.commit()


@app.put("/update_details", status_code=status.HTTP_204_NO_CONTENT)
async def update_details(user: user_dependency, db: db_dependency, update_user_details_request: UpdateUserDetailsRequest):
    existing_user: Users = db.query(Users).filter(Users.id == user["id"]).one_or_none()
    existing_user.phone_number = update_user_details_request.phone_number
    existing_user.address = update_user_details_request.address
    db.add(existing_user)
    db.commit()
