from sqlalchemy.orm import Session, Query as sqlQuery
import database.sqlModels as sqlModels
from database.db_clients import PostgresDatabase
from typing import Any

postgresManager = PostgresDatabase()


def get_user(user_id: int):
    sessionLocal: Session = postgresManager.get_session()
    session = sessionLocal()
    user: sqlModels.Users = session.query(sqlModels.Users).filter(
        sqlModels.Users.id == user_id).first()
    return user


def get_comments(recipe_id: str):
    sessionLocal: Session = postgresManager.get_session()
    session = sessionLocal()
    comments = session.query(sqlModels.Comments).filter(
        sqlModels.Comments.recipe_id == recipe_id)
    # group sub comments
    comment_groups = {}
    for item in comments:
        comment: sqlModels.Comments | Any = item
        if comment.comment_id is not None:
            sub_comments = comment_groups.get(comment.comment_id, [])
            sub_comments.append(comment)
            setattr(comment, "owner", {"username": comment.user.user_name,
                                       "id": comment.user.id,
                                       "email": comment.user.email})
            comment_groups[comment.comment_id] = sub_comments

    # move sub comments to each parent
    res = []
    for item in comments:
        comment: sqlModels.Comments | Any = item
        if comment.is_sub:
            continue
        elif comment.id in comment_groups:
            setattr(comment, "replies", comment_groups[comment.id])
        setattr(comment, "owner", {"username": comment.user.user_name,
                                   "id": comment.user.id,
                                   "email": comment.user.email})
        res.append(comment)
    return res
