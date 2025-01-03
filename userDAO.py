import pymongo
import bcrypt

class UserDAO():
    def __init__(self, db):
        self.db = db
        self.col = db["users"]
    def newUser(self,name, password):
        self.col.insert_one({
            "username":name,
            "password":bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()),
            "admin":False
        })

    def checkPW(self, name, password):
        user = self.col.find_one({"username":name})
        return bcrypt.checkpw(password.encode("utf-8"),user["password"])

    def giveAdmin(self,name):
        self.col.update_one({"username":name},{"$set":{"admin":True}})

    def checkAdmin(self,name):
        return self.col.find_one({"username":name})["admin"]

    def deleteUser(self, name):
        self.col.delete_one({"username":name})

client = pymongo.MongoClient("mongodb://localhost:27017/")
ud = UserDAO(client.get_database("boardgames"))
