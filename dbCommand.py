from pymongo import MongoClient
from datetime import datetime
# from mongothon import Schema
import mongothon

import config

client = MongoClient(config.MONGO_URL)
# dbNews = client['lovel-up']
db = client['twitter_bot']

user_schema = mongothon.Schema({
    "id":               {"type": basestring, "required": True},
    "name":             {"type": basestring},
    "date_followed":    {"type": datetime },
    "date_unfollowed":  {"type": datetime },
    "following":        {"type": bool},
    "following_me":     {"type": bool}
})


User = mongothon.create_model(user_schema, db['users'])

def get_user_by_id(id):
    print id
    return User.find_one({'id': str(id)})


def add_user(user):

    newUser = User({
                "id": str(user['id']),
                "name": user['name'],
                "following": True
            })
    newUser.save()

def add_user_id(id):
    newUser = User({
        "id": str(id),
        "following": False,
        "following_me": True
    })
    newUser.save()

def update_following_me_true(id):
    User.update({"id": id}, {"following_me": {"$set": True}})

def update_following_me(user):
    usr =  User.find_one({'id': user['id_str']})
    usr['following_me'] = False
    usr.save()