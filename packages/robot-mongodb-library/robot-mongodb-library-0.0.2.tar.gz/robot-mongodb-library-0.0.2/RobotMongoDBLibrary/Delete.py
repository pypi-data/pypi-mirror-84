import pymongo
from bson.objectid import ObjectId

def DeleteOne(con,fillter):
    try:
        db=pymongo.MongoClient("mongodb://"+con["username"]+":"+con["password"]+"@"+con["host"]+":"+con["port"])[con["database"]][con["collection"]]
        if db.delete_one(fillter).deleted_count != 0:return "DELETED SUCCESS"
        return "DATA NOT FOUND"
    except:
        print("error insert database")
        return "DELETED ERROR"

def DeleteOneByID(con,id):
    try:
        db=pymongo.MongoClient("mongodb://"+con["username"]+":"+con["password"]+"@"+con["host"]+":"+con["port"])[con["database"]][con["collection"]]
        if db.delete_one({"_id":ObjectId(id)}).deleted_count != 0:return "DELETED SUCCESS"
        return "DATA NOT FOUND"
    except:
        return "DELETED ERROR"