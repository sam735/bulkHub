import pdb
from typing import Dict
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

#db_url = "mongodb+srv://@{0}/bulkHub?retryWrites=true&w=majority".format(os.environ.get())

client = MongoClient(os.environ.get('DB_URL'))
db = client['bulkHub-db']

def get_db():
    try:
        yield db
    finally:
        client.close()

def get_user(paylaod:Dict):
    return list(db.user.find(paylaod))

def insert_user_details(user_details:Dict):
    return db.user.insert(user_details)

def create_address(address:Dict):
    return db.address.insert(address)

def get_address(payload:Dict):
    return list(db.address.find(payload))

def update_address(query:Dict,payload:Dict):

    adress_details = {}
    for key,value in payload.items():
        if key =='is_default':
            adress_details[key] = value
        elif key == 'phone':
            adress_details[key] = value
        else:
            adress_details['user_address.' + key] = value
    
    update_dict = {
        '$set':adress_details
    }
    return db.address.update(query,update_dict)

def delete_address(query:Dict):
    return db.address.remove(query)

def update_user_detail(query,payload:Dict):
    update_dict = {
        '$set':payload
    }
    return db.user.update(query,update_dict)

def create_seller(seller_dtails:Dict):
    return db.seller.insert(seller_dtails)

def get_seller(query:Dict):
    return list(db.seller.find(query))

def create_seller_address(address:Dict):
    return db.seller_address.insert(address)

def update_seller_address(query:Dict,payload:Dict):

    update_dict = {
        '$set':payload
    }
    return db.seller_address.update(query,update_dict)

def get_seller_address(query):
    return list(db.seller_address.find(query))