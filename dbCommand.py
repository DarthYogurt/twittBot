from pymongo import MongoClient
from datetime import datetime
# from mongothon import Schema
import mongothon
from datetime import timedelta

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
    return User.find_one({'id': str(id)})

def get_users( following, following_me, days ):
    users = []

    query = { "following": following, "following_me": following_me }
    if following == True and following_me == False:
        query['date_followed'] = { '$lt': datetime.utcnow() - timedelta( days=days )}
    if following == False and following_me == False:
        query['date_unfollowed'] = { '$lt': datetime.utcnow() - timedelta( days=days )}

    for u in User.find(query):
        users.append(u)
    return users

def add_user(user):
    newUser = User({
                "id": str(user['id']),
                "name": user['name'],
                "following": True,
                "date_followed": datetime.utcnow()
            })
    newUser.save()

def add_user_id(id):
    newUser = User({
        "id": str(id),
        "following": False,
        "following_me": True
    })
    newUser.save()

def update_following_me(id, following_me):
    usr =  User.find_one({'id': str(id)})
    usr['following_me'] = following_me
    usr.save()

def update_following(id, following):
    usr = User.find_one({'id': str(id)})

    usr['following'] = following
    if following:
        usr['date_followed'] = datetime.utcnow()
    else:
        usr['date_unfollowed'] = datetime.utcnow()
    usr.save()



# print get_users(True, True, 2)