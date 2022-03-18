import os
import sys

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

CREDENTIAL = os.environ["MONGO_CREDENTIAL"]

if not CREDENTIAL:
    print("MONGO_CREDENTIAL is not set")
    sys.exit(-1)

client = MongoClient(
    f"mongodb+srv://{CREDENTIAL}@toittacluster.dfekh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
    server_api=ServerApi("1"),
)
db = client["ToittaDB"]
