from typing import Dict
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

#db_url = "mongodb+srv://@{0}/bulkHub?retryWrites=true&w=majority".format(os.environ.get())
client = MongoClient(os.environ.get('DB_URL').strip())
db = client['bulkHub-db']

def get_db():
    try:
        yield db
    finally:
        client.close()

def get_user(paylaod:Dict):
    return list(db.user.find(paylaod))

def insert_user_details(user_details:Dict):
    user_details['createdAt'] = datetime.now()
    return db.user.insert(user_details)

def create_address(address:Dict):
    address['createdAt'] = datetime.now()
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
    adress_details['updatedAt'] = datetime.now()
    update_dict = {
        '$set':adress_details
    }
    return db.address.update(query,update_dict)

def delete_address(query:Dict):
    return db.address.remove(query)

def update_user_detail(query,payload:Dict):
    payload['updatedAt'] = datetime.now()
    update_dict = {
        '$set':payload
    }
    return db.user.update(query,update_dict)

def create_seller(seller_dtails:Dict):
    seller_dtails['createdAt'] = datetime.now()
    return db.seller.insert(seller_dtails)

def get_seller(query:Dict):
    return list(db.seller.find(query))

def create_seller_address(address:Dict):
    address['createdAt'] = datetime.now()
    return db.seller_address.insert(address)

def update_seller_address(query:Dict,payload:Dict):
    payload['updatedAt'] = datetime.now()
    update_dict = {
        '$set':payload
    }
    return db.seller_address.update(query,update_dict)

def get_seller_address(query):
    return list(db.seller_address.find(query))

def create_product_category_type(product_category_details:Dict):
    product_category_details['createdAt'] = datetime.now()
    return db.product_category.insert(product_category_details)

def get_product_category():
    return list(db.product_category.find())

def get_each_product_category(query:Dict):
    return list(db.product_category.find(query))

def update_product_category(query:Dict, payload:Dict):
    payload['updatedAt'] = datetime.now()
    update_dict = {
        '$set': payload
    }
    return db.product_category.update(query, update_dict)

def delete_product_category(query:Dict):
    return db.product_category.remove(query)