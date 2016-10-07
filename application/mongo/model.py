import bcrypt
import os
import pymongo

from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

FORMS_MONGO_HOST = os.environ.get("FORMS_MONGO_HOST", "localhost")

client = MongoClient(host=FORMS_MONGO_HOST)

class Profile(object):

    def __init__(self):
        self.collection = client.pixelio.profile

    def create(self, mac_address, coordinates):
        return self.collection.insert_one({
            'mac_address': mac_address,
            'coordinates': coordinates
        })
        
    def get_all(self):
        return self.collection.find()

    def get_profile_by_id(self, id):
        return self.collection.find_one({"_id": form_id})
    
    def get_profile_by_mac_address(self, mac_address):
        return self.collection.find_one({"mac_address": mac_address})
    
    # def update_form_info(self, form_id, info):
    #     return self.collection.update({'_id': form_id}, {'$set': info})

    def remove_all(self):
        res = self.collection.delete_many({})
        print 'Form Deleted ', res.deleted_count
        return res
