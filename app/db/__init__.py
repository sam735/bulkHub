import os
from pymongo import MongoClient

#db_url = "mongodb+srv://@{0}/bulkHub?retryWrites=true&w=majority".format(os.environ.get())

client = MongoClient(os.environ.get('MONGO_DB_READ_URI'))
db = client['litmus-db']

def get_db():
    try:
        yield db
    finally:
        client.close()
