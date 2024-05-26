from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from core.database import SessionLocal
from typing import Annotated
from core.models import Users, PassTokens
from core.auth import get_current_user, bcrypt_context
from core.emailer import send_email
from typing import Any
from uuid import uuid4
from core.utils import EnvManager
import datetime

env = EnvManager()

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
auth_dependency = Annotated[dict, Depends(get_current_user)]


def check_login(user):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authenticated Failed!')


def create_token_pass(user: Users, db: Session):
    token: PassTokens = PassTokens(user_id=user.id, token=str(uuid4()))
    db.add(token)
    db.commit()
    return token.token


def disable_token(token: PassTokens, db: Session):
    token.active = False
    db.commit()
    db.refresh(token)


def validate_token(token: PassTokens, db: Session):
    base_except = HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Token not longer valid!")
    if not token.active:
        raise base_except
    cur_date = datetime.datetime.now() + datetime.timedelta(
        minutes=token.expiration)
    if token.created_date > cur_date:
        disable_token(token, db)
        raise base_except


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(user: auth_dependency, db: db_dependency,
                    how_many: int = 10):
    # TODO: if we got bunch of user registered in a future we
    #  will need pagination
    check_login(user)
    users = db.query(Users).limit(how_many).all()
    return users


@router.patch("/is_active", status_code=status.HTTP_202_ACCEPTED)
async def deactivate_user(user: auth_dependency, db: db_dependency,
                          user_id: int, active_status: bool):
    check_login(user)
    admin_usr: Users = db.query(Users).filter(
        Users.id == user.get('id')).first()
    if admin_usr and not admin_usr.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'{admin_usr.user_name} not allowed '
                                   f'to perform this action!')
    f_user: Users = db.query(Users).filter(Users.id == user_id).first()
    if not f_user:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'user not found with id {user_id}')
    f_user.is_active = active_status
    db.commit()
    db.refresh(f_user)
    return {
        "message": f"user successful {'Activated' if active_status else 'Disabled'}"}


@router.get("/reset_password_request", status_code=status.HTTP_200_OK)
async def reset_password_request(db: db_dependency, username: str = None,
                                 email: str = None):
    user: Users | Any = None
    if username:
        user = db.query(Users).filter(Users.user_name == username).first()
    if not user and email:
        user = db.query(Users).filter(Users.email == email).first()
    if user:
        token = create_token_pass(user, db)
        base = env.get_env('FRONTEND_URL', 'http://localhost:8000')
        url = f"{base}/reset_pass?token={token}"
        await send_email([user.email], "reset password",
                         f"Reset Password here {url}",
                         template="templates/emails/request_reset_pass.html",
                         data={"url": url})
        return {"message": "reset password email sent!"}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something went wrong!")


@router.patch("/update_pass", status_code=status.HTTP_200_OK)
async def rest_password(db: db_dependency, token: str, password: str):
    base_except = HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                                detail="Token not valid or not found!")
    f_token: PassTokens = db.query(PassTokens).filter(
        PassTokens.token == token).first()
    if not f_token:
        raise base_except
    validate_token(f_token, db)
    user: Users = db.query(Users).filter(
        Users.id == f_token.user_id).first()
    user.hashed_password = bcrypt_context.hash(password)
    db.commit()
    db.refresh(user)
    disable_token(f_token, db)
    return {"message": "Reset password successful!"}
