from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from starlette import status
from core.database import SessionLocal
from typing import Annotated
from core.models import StarsRecipe
from core.auth import get_current_user
from typing import Any, Optional
from core.utils import EnvManager
import datetime
from pydantic import BaseModel
from core.utils import check_login

env = EnvManager()

router = APIRouter(
    prefix="/stars",
    tags=["stars"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
auth_dependency = Annotated[dict, Depends(get_current_user)]


class Star(BaseModel):
    user_id: int
    recipe_id: str
    stars: int


@router.get("/", status_code=status.HTTP_200_OK)
async def get_stars(db: db_dependency, recipe_id: str):
    stars = db.query(func.avg(StarsRecipe.stars)).filter(
        StarsRecipe.recipe_id == recipe_id).scalar()
    if not stars:
        return {"total": 0}
    return {"total": stars}


@router.post("/", status_code=status.HTTP_200_OK)
async def star_recipe(db: db_dependency, user: auth_dependency, request: Star):
    check_login(user)
    kargs = {
        "recipe_id": request.recipe_id,
        "user_id": user.get('id'),
        "stars": request.stars
    }
    star_save_update = StarsRecipe(**kargs)
    db.merge(star_save_update)
    db.commit()
    return star_save_update
