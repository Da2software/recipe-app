import json
from core.utils import EnvManager
from database.db_clients import MongoDatabase
import pandas as pd
import threading

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
        new_items.append({
            'title': item['title'],
            'ingredients': json.loads(item['ingredients']),
            'directions': json.loads(item['directions']),
            'NER': json.loads(item['NER'])
        })
    collection.insert_many(new_items)
    print(f'{len(new_items)} added.')


def run():
    num_threads = 4
    documents = df[0:1001]
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
