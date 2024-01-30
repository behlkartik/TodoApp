import datetime

from fastapi import APIRouter, Depends, status, HTTPException
import typing as t
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import CreateUserRequest, JwtToken
from models import Users
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta

SECRET_KEY = "942e380afb42cf4e404d38ec00543178f5677ff9d9da494a606ec87166347449"
ALGORITHM = "HS256"

app = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


db_dependency = t.Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db: Session):
    existing_user = db.query(Users).filter(Users.username == username.casefold()).one_or_none()
    if not existing_user:
        return None
    password_check = bcrypt_context.verify(password, existing_user.hashed_pwd)
    if not password_check:
        return None
    return existing_user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    claims = {
        "sub": username, "id": user_id, "role": role
    }
    expires = datetime.datetime.utcnow() + expires_delta
    claims.update({"exp": expires})
    return jwt.encode(claims, key=SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: t.Annotated[str, Depends(oauth2_bearer)]):
    print("get current user called!!!")
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload.get("sub")
        user_id = payload.get("id")
        user_role = payload.get("role")
        print("payload is:", payload)
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials")
        return {"username": username, "id": user_id, "role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials")


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    try:
        hashpwd = bcrypt_context.hash(create_user_request.password)
        new_user = Users(
            email=create_user_request.email,
            username=create_user_request.username,
            first_name=create_user_request.first_name,
            last_name=create_user_request.last_name,
            hashed_pwd=hashpwd,
            role=create_user_request.role
        )
        db.add(new_user)
        db.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/token", status_code=status.HTTP_200_OK, response_model=JwtToken)
async def get_token(db: db_dependency, form_data: t.Annotated[OAuth2PasswordRequestForm, Depends()]):
    authenticated_user: t.Optional[Users] = authenticate_user(form_data.username, form_data.password, db)
    if not authenticated_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Couldn't validate credentials")
    token = create_access_token(authenticated_user.username, authenticated_user.id, authenticated_user.role, expires_delta=timedelta(minutes=1))
    print(token)
    return {"access_token": token, "token_type": "Bearer"}

# @app.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
# async def validate_token(db: db_dependency, form_data: t.Annotated[OAuth2PasswordRequestForm, Depends()]):
#     # existing_user = db.query(Users).filter(Users.email == login_user_request.email.casefold()).one_or_none()
#     # password_check = bcrypt_context.verify(login_user_request.password, existing_user.hashed_pwd)
#     # if not existing_user or not password_check:
#     #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username or Password incorrect!!!")
#     # return {"user": login_user_request.email, "authenticated": True}
#     authenticated_user: Users = authenticate_user(form_data.username, form_data.password, db)
#     if not authenticated_user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Username or Password incorrect!!!")
#     token = create_access_token(authenticated_user.username, authenticated_user.id, expires_delta=timedelta(minutes=1))
#     return {"token": token, "type": "Bearer"}