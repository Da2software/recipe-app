import graphene
from core.utils import EnvManager
from bson.objectid import ObjectId
from database.db_clients import MongoDatabase, PostgresDatabase
from sqlalchemy.orm import Session, Query as sqlQuery
from sqlalchemy import func
from core.processes import get_user, get_comments
import database.sqlModels as sqlModels

ENV = EnvManager()
client = MongoDatabase().get_connection()
db = client[ENV.get_env("MONGO_DB")]

postgresManager = PostgresDatabase()
sqlBase = postgresManager.get_connection()


class User(graphene.ObjectType):
    id = graphene.Int()
    email = graphene.String()
    user_name = graphene.String()


class Recipe(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    image = graphene.String()
    ingredients = graphene.List(graphene.String)
    directions = graphene.List(graphene.String)
    NER = graphene.List(graphene.String)
    author_id = graphene.Int(required=False, default_value=0)
    category = graphene.String(required=False)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    owner = graphene.Field(User)
    comments = graphene.List(lambda: Comment)


class RecipesPage(graphene.ObjectType):
    recipes = graphene.List(Recipe)
    total = graphene.Int()


class Comment(graphene.ObjectType):
    id = graphene.ID()
    recipe_id = graphene.String()
    text = graphene.String()
    user_id = graphene.Int()
    is_sub = graphene.Boolean()
    comment_id = graphene.Int()
    created_at = graphene.DateTime()
    replies = graphene.List(lambda: Comment)
    owner = graphene.Field(User)


class Stars(graphene.ObjectType):
    recipe_id = graphene.String()
    total = graphene.Int()


class Query(graphene.ObjectType):
    recipes_page = graphene.Field(RecipesPage,
                                 id=graphene.String(),
                                 title=graphene.String(),
                                 ingredients=graphene.List(graphene.String),
                                 directions=graphene.List(graphene.String),
                                 image=graphene.String(),
                                 NER=graphene.List(graphene.String),
                                 author_id=graphene.Int(),
                                 categories=graphene.List(graphene.String),
                                 most_recent=graphene.Boolean(),
                                 page=graphene.Int(),
                                 size=graphene.Int())
    users = graphene.List(User, id=graphene.Int(), email=graphene.String(),
                          user_name=graphene.String())

    comments = graphene.List(Comment, id=graphene.Int(),
                             recipe_id=graphene.String(),
                             text=graphene.String(), user_id=graphene.Int(),
                             is_sub=graphene.Boolean(),
                             comment_id=graphene.Int(),
                             created_at=graphene.DateTime())

    stars = graphene.Field(Stars, recipe_id=graphene.String())

    def resolve_recipes_page(self, info, id=None, title=None, ingredients=None,
                        author_id=None, categories=None, most_recent=False,
                        page=1, size=10):

        skip = (page - 1) * size
        limit = size

        requested_fields = [field.name.value for field in
                            info.field_nodes[0].selection_set.selections]

        mongo_recipes = db[ENV.get_env("MONGO_COLLECTION")]

        query = {}
        if id:
            query["_id"] = ObjectId(id)
        if title:
            query["title"] = {"$regex": title, "$options": "i"}
        if author_id:
            query["author_id"] = author_id
        if categories:
            query["category"] = {"$in": categories}
        if ingredients:
            regex_pattern = "|".join(ingredients)
            query["ingredients"] = {
                "$regex": regex_pattern,
                "$options": "i"
            }
        base_query = mongo_recipes.find(query)
        total = 0
        if "total" in requested_fields:
            # for optimization, if we don't need it we can avoid it
            total = mongo_recipes.count_documents(query)
        recipes = base_query.skip(skip).limit(limit)
        if most_recent:
            recipes = recipes.sort({"created_at": -1})
        res = []
        for recipe in recipes:
            kargs = {
                "id": str(recipe["_id"]),
                "title": recipe["title"],
                "image": recipe.get("image", None),
                "ingredients": recipe["ingredients"],
                "directions": recipe["directions"],
                "NER": recipe["NER"],
                "author_id": recipe.get("author_id", None),
                "category": recipe.get("category", None),
                "created_at": recipe["created_at"],
                "updated_at": recipe["updated_at"]
            }
            if "owner" in requested_fields and kargs["author_id"]:
                kargs["owner"] = get_user(kargs["author_id"])
            if "comments" in requested_fields:
                comments = get_comments(recipe_id=kargs["id"])
                kargs["comments"] = comments

            res.append(Recipe(**kargs))
        return {"recipes": res, "total": total}

    def resolve_users(self, info, id=None, email=None, user_name=None):
        sessionLocal: Session = postgresManager.get_session()
        session = sessionLocal()
        query: sqlQuery = session.query(sqlModels.Users)

        if id:
            query = query.filter(sqlModels.Users.id == id)
        if email:
            query = query.filter(sqlModels.Users.email == email)
        if user_name:
            query = query.filter(sqlModels.Users.user_name == user_name)
        users = query.all()
        session.close()
        return users

    def resolve_comments(self, info, recipe_id: str):
        res = get_comments(recipe_id=recipe_id)
        return res

    def resolve_stars(self, info, recipe_id: str):
        sessionLocal: Session = postgresManager.get_session()
        session = sessionLocal()
        stars = session.query(func.avg(sqlModels.StarsRecipe.stars)).filter(
            sqlModels.StarsRecipe.recipe_id == recipe_id).scalar()
        if not stars:
            return {"total": 0, "recipe_id": recipe_id}
        return {"total": stars, "recipe_id": recipe_id}


schema = graphene.Schema(query=Query)
