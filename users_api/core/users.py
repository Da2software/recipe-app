from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from core.database import SessionLocal
from typing import Annotated
from core.models import Users
from core.auth import get_current_user

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


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(user: auth_dependency, db: db_dependency,
                    how_many: int = 10):
    # TODO: if we got bunch of user registered in a future we
    #  will need pagination
    if user is None:
        raise HTTPException(status_code=401, detail='Authenticated Failed!')
    users = db.query(Users).limit(how_many).all()
    return users
