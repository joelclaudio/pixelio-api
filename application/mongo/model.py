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
        self.collection = client.seed_rocket.profile

    def create(self, email):
        return self.collection.insert_one({
            'email': email 
        })

    def get_all(self):
        return self.collection.find()

    def get_profile_by_id(self, id):
        return self.collection.find_one({"_id": id})

    def get_profile_by_email(self, email):
        return self.collection.find_one({"email": email})
    
    def remove_all(self):
        res = self.collection.delete_many({})
        print 'Form Deleted ', res.deleted_count
        return res
