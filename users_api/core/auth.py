from datetime import timedelta, datetime
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from core.database import SessionLocal
from core.models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from core.utils import EnvManager

env = EnvManager()

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = env.get_env("SECRET_KEY")
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def auth_user(user_name: str, password: str, db: Session):
    user: Users | Any = db.query(Users).filter(
        Users.user_name == user_name).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.get("/")
def get_current_user(token: Annotated[str, Depends(oauth2_bearer)],
                     db: db_dependency):
    no_valid_user_except = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate user.')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('id')
        user: Users = db.query(Users).filter(Users.id == user_id).first()
        if user is None:
            raise no_valid_user_except
        return {'username': user.user_name, 'id': user_id, 'email': user.email}
    except JWTError:
        raise no_valid_user_except


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, request: CreateUserRequest):
    new_user = Users(
        user_name=request.username,
        email=request.email,
        hashed_password=bcrypt_context.hash(request.password),
    )

    db.add(new_user)
    db.commit()
    return {"message": f"User {new_user.user_name} successful created!"}


@router.post("/token", response_model=Token)
async def login_for_access_token(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency):
    user = auth_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.user_name, user.id, timedelta(minutes=20))
    response.set_cookie(key="session_token", value=token)
    return {'access_token': token, 'token_type': 'bearer'}


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("session_token")
    return {"message": "logout successful!"}
