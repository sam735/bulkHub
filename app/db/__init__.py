from typing import Dict
import os
from pymongo import MongoClient

#db_url = "mongodb+srv://@{0}/bulkHub?retryWrites=true&w=majority".format(os.environ.get())

client = MongoClient(os.environ.get('DB_URL'))
db = client['bulkHub-db']

def get_db():
    try:
        yield db
    finally:
        client.close()

def get_user(paylaod:Dict):
    try:
        return list(db.user.find(paylaod))
    except Exception as e:
        return None

def insert_user_details(user_details:Dict):
    return db.user.insert(user_details)
