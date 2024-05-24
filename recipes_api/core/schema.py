import graphene
from core.utils import EnvManager
from bson.objectid import ObjectId
from database.db_clients import MongoDatabase
import re

ENV = EnvManager()
client = MongoDatabase().get_connection()
db = client[ENV.get_env("MONGO_DB")]


class Recipe(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    ingredients = graphene.List(graphene.String)
    directions = graphene.List(graphene.String)
    NER = graphene.List(graphene.String)
    author_id = graphene.Int(required=False)
    category = graphene.String(required=False)


class Query(graphene.ObjectType):
    recipes = graphene.List(Recipe, id=graphene.ID(), title=graphene.String(),
                            ingredients=graphene.List(graphene.String),
                            author_id=graphene.Int(),
                            categories=graphene.List(graphene.String))

    def resolve_recipes(self, info, id=None, title=None, ingredients=None,
                        autor_id=None, categories=None):
        mongo_recipes = db[ENV.get_env("MONGO_COLLECTION")]

        query = {}
        if id:
            query["_id"] = ObjectId(id)
        if title:
            query["title"] = {"$regex": title, "$options": "i"}
        if autor_id:
            query["author_id"] = autor_id
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


schema = graphene.Schema(query=Query)
