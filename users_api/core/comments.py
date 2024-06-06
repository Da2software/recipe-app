from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from core.database import SessionLocal
from typing import Annotated
from core.models import Users, Comments
from core.auth import get_current_user, bcrypt_context
from core.emailer import send_email
from typing import Any, Optional
from uuid import uuid4
from core.utils import EnvManager
import datetime
from pydantic import BaseModel
from core.utils import check_login

env = EnvManager()

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
auth_dependency = Annotated[dict, Depends(get_current_user)]


class CommentRequest(BaseModel):
    recipe_id: str
    text: str
    comment_id: Optional[int] = None


@router.get("/", status_code=status.HTTP_200_OK)
async def get_comment(db: db_dependency, recipe_id: str):
    comments = db.query(Comments).filter(Comments.recipe_id == recipe_id).all()

    if not comments:
        raise HTTPException(status_code=404,
                            detail="Comments not found for the given recipe ID")
    # group sub comments
    comment_groups = {}
    for item in comments:
        comment: Comments | Any = item
        if comment.comment_id is not None:
            sub_comments = comment_groups.get(comment.comment_id, [])
            sub_comments.append(comment)
            comment_groups[comment.comment_id] = sub_comments
    # move sub comments to each parent
    res = []
    for item in comments:
        comment: Comments | Any = item
        if comment.is_sub:
            continue
        elif comment.id in comment_groups:
            setattr(comment, "replies", comment_groups[comment.id])
        res.append(comment)
    return res


@router.post("/", status_code=status.HTTP_200_OK)
async def add_comment(db: db_dependency, user: auth_dependency,
                      request: CommentRequest):
    check_login(user)
    kargs = {
        "recipe_id": request.recipe_id,
        "user_id": user.get('id'),
        "text": request.text
    }
    if request.comment_id:
        kargs["comment_id"] = request.comment_id
        kargs["is_sub"] = True
    new_comment = Comments(**kargs)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
