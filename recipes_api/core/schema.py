import graphene
from core.utils import EnvManager
from bson.objectid import ObjectId
from database.db_clients import MongoDatabase, PostgresDatabase
from sqlalchemy.orm import Session, Query as sqlQuery
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
    ingredients = graphene.List(graphene.String)
    directions = graphene.List(graphene.String)
    NER = graphene.List(graphene.String)
    author_id = graphene.Int(required=False, default_value=0)
    category = graphene.String(required=False)


class Query(graphene.ObjectType):
    recipes = graphene.List(Recipe, id=graphene.ID(), title=graphene.String(),
                            ingredients=graphene.List(graphene.String),
                            author_id=graphene.Int(),
                            categories=graphene.List(graphene.String))
    users = graphene.List(User, id=graphene.Int(), email=graphene.String(),
                          user_name=graphene.String())

    def resolve_recipes(self, info, id=None, title=None, ingredients=None,
                        author_id=None, categories=None):
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

        recipes = mongo_recipes.find(query)
        res = []
        for recipe in recipes:
            res.append(Recipe(
                id=str(recipe["_id"]),
                title=recipe["title"],
                ingredients=recipe["ingredients"],
                directions=recipe["directions"],
                NER=recipe["NER"]
            ))
        return res

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


schema = graphene.Schema(query=Query)
