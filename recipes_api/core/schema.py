import graphene
from core.utils import EnvManager
from bson.objectid import ObjectId
from database.db_clients import MongoDatabase

ENV = EnvManager()
client = MongoDatabase().get_connection()
db = client[ENV.get_env("MONGO_DB")]


class Recipe(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    ingredients = graphene.List(graphene.String)
    directions = graphene.List(graphene.String)
    NER = graphene.List(graphene.String)


class Query(graphene.ObjectType):
    recipes = graphene.List(Recipe)

    @staticmethod
    def resolve_recipes(*args, **kwargs):
        mongo_recipes = db[ENV.get_env("MONGO_COLLECTION")]
        recipes = mongo_recipes.find()
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
