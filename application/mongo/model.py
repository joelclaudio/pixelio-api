import bcrypt
import os
import pymongo

from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

FORMS_MONGO_HOST = os.environ.get("FORMS_MONGO_HOST", "localhost")

client = MongoClient(host=FORMS_MONGO_HOST, connect=False)

class Profile(object):

    def __init__(self):
        self.collection = client.pixelio.profile

    def create(self, mac_address, location):
        if self.get_profile_by_mac_address(mac_address) is None:
            return self.collection.insert_one({
                'macAddress': mac_address,
                'location': location,
                'is_active': True,
                'size': 10
            })
        return self.update_profile(mac_address, location)

    def get_all(self):
        return self.collection.find()

    def get_profile_by_id(self, id):
        return self.collection.find_one({"_id": form_id})

    def get_profile_by_mac_address(self, mac_address):
        return self.collection.find_one({"macAddress": mac_address})
    
    def get_all_active_players(self):
        return self.collection.find()
    
    def get_tmp_profile(self):
        return self.collection.find_one()
    
    def update_profile(self, mac_address, location):
        return self.collection.update({'macAddress': mac_address}, {'$set': {
                'macAddress': mac_address,
                'location': location
            }})

    def remove_all(self):
        res = self.collection.delete_many({})
        print 'Form Deleted ', res.deleted_count
        return res
