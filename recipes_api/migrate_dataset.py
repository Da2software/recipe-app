import json
from core.utils import EnvManager
from database.db_clients import MongoDatabase
import pandas as pd
import threading
from datetime import datetime

ENV = EnvManager()

# extract cv
data = pd.read_csv(r"RecipeNLG_dataset.csv")
df = pd.DataFrame(data)
df = df.reset_index()
client = MongoDatabase().get_connection()
db = client[ENV.get_env("MONGO_DB")]
collection = db[ENV.get_env("MONGO_COLLECTION")]


def inset_collection(chunk):
    new_items = []
    for idx, item in chunk.iterrows():
        current_time = datetime.utcnow()
        new_items.append({
            'title': item['title'],
            'ingredients': json.loads(item['ingredients']),
            'directions': json.loads(item['directions']),
            'description': 'This delightful dish offers a symphony of flavors that dance on your palate. Each bite brings a harmonious blend of textures and aromas, leaving you craving more. Perfect for any occasion, it promises to be a memorable culinary experience that will delight all who taste it.',
            'image': 'https://copilot.microsoft.com/images/create/a-dish-with-a-very-tasty-food-in-hyper-realistic-s/1-66648c1ea69f4fe08635a7be4c58acea?id=eCbN7DP7gwpLzRK8%2bbnFrg%3d%3d&view=detailv2&idpp=genimg&idpclose=1&thId=OIG4.TgwL..JLzgTwAJQjubgl&FORM=SYDBIC',
            'NER': json.loads(item['NER']),
            'created_at': current_time,
            'updated_at': current_time
        })
    collection.insert_many(new_items)
    print(f'{len(new_items)} added.')


def run():
    num_threads = 4
    documents = df[0:2001]
    chunk_size = len(documents) // num_threads
    chunks = [documents[i:i + chunk_size] for i in
              range(0, len(documents), chunk_size)]

    threads = []
    for c_collection in chunks:
        thread = threading.Thread(target=inset_collection,
                                  args=(c_collection,))
        threads.append(thread)
        thread.start()


def query_items():
    collection.find_one()


if __name__ == '__main__':
    run()
    query_items()
