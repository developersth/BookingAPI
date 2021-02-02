from os import abort
import pymongo
from flask import Flask , jsonify
import datetime
from python_json_config import ConfigBuilder
import bcrypt
import uuid
builder = ConfigBuilder()
config = builder.parse_config('bin/config.json')

class MongoDb:
    def __init__(self):
        print("Calling parent constructor")
    def __del__(self):
        print('Object was destroyed')

    def connectDb(self):
        try:
            str_conn = self.getConnStrMongoDB()
            conn = pymongo.MongoClient(str_conn,serverSelectionTimeoutMS=5000)
            conn.server_info()

            return conn
        except Exception as e:
            abort(500)

    def getDatabaseName(self):
        return config.mongodb.database

    def getConnStrMongoDB(self):
        if config.mongodb.srv is True:
            res = "mongodb+srv://%s:%s@%s/%s?retryWrites=true&w=majority" % (
                config.mongodb.username,
                config.mongodb.password,
                config.mongodb.host,
                config.mongodb.database_auth
            )
        else:
            res = "mongodb://%s:%s@%s:%s" % (
                config.mongodb.username,
                config.mongodb.password,
                config.mongodb.host,
                config.mongodb.database_auth,
                config.mongodb.port
            )
        return res

    def getConfig(self):
        return config

    def insertUserDB(self,username,password,email,mobile,status,imgUrl,role,roleName):
        conn = self.connectDb()
        find_username = conn[self.getDatabaseName()]["users"].find_one({"username": "%s" % username})
        find_email = conn[self.getDatabaseName()]["users"].find_one({"email": "%s" % email})
        find_mobile = conn[self.getDatabaseName()]["users"].find_one({"mobile": "%s" % mobile})
        u_uuid = uuid.uuid4()
        if not find_username is None:
            vMsg = "USERNAME_TAKEN"
            vCheck = False
            return vCheck, vMsg
        if not find_email is None:
            vMsg = "EMAIL_TAKEN"
            vCheck = False
            return vCheck, vMsg
        if not find_mobile is None:
            vMsg = "MOBILE_TAKEN"
            vCheck = False
            return vCheck, vMsg
        # Insert Data
        regis = conn[self.getDatabaseName()]["users"].insert_one({
                "uuid"      : "%s" % u_uuid,
                "username"  : "%s" % username,
                "password"  : "%s" % bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                "email"     : "%s" % email,
                "mobile"    : "%s" % mobile,
                "status"    : status,
                "imgUrl"    : "%s" % imgUrl,
                "lastLogin" : datetime.datetime.now(),
                "creatAt"   : datetime.datetime.now(),
                "updateAt"  : datetime.datetime.now(),
                "details": {
                    "role": "%s" % role,
                    "roleName": "%s" % roleName
                },
            })

        if not regis is None:
            vMsg = "SUCCESS"
            vCheck = True
            return vCheck, vMsg

    def checkuser(self, user, passwd):
        conn = self.connectDb()
        # Get Username
        data = conn[self.getDatabaseName()]["users"].find_one({
            "username": "%s" % user,
        })
        if not data is None:
            if bcrypt.checkpw(password=passwd.encode("utf-8"), hashed_password=data["password"].encode("utf-8")):
                return data

        return None

