import pymongo
import bcrypt
import pymongo.database
import logging

class UserDAO():
    def __init__(self, db):
        self.db = db
        self.col = db["users"]
        logging.basicConfig(filename="database.log", encoding='utf-8',level=logging.INFO, format='%(asctime)s :: %(message)s')
    def newUser(self,name, password):
        self.col.insert_one({
            "username":name,
            "password":bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()),
            "admin":False
        })
        logging.info('Added user %s to users collection',name)

    def checkPW(self, name, password):
        if self.userExists(name):
            user = self.col.find_one({"username":name})
            attempt = bcrypt.checkpw(password.encode("utf-8"),user["password"])
            logging.info("login as %s is %s",name, attempt)
            return attempt
        else: 
            return False

    def giveAdmin(self,name):
        self.col.update_one({"username":name},{"$set":{"admin":True}})
        logging.info('%s has received admin access',name)

    def removeAdmin(self,name):
        self.col.update_one({"username":name},{"$set":{"admin":False}})
        logging.info('Removed admin access from %s',name)

    def checkAdmin(self,name):
        return self.col.find_one({"username":name})["admin"]

    def deleteUser(self, name):
        self.col.delete_one({"username":name})
        logging.info("%s has been removed from users",name)

    def userExists(self, name):
        try:
            self.col.find({"username":name}).next()
            return True
        except StopIteration:
            return False
        
    def getUser(self,name):
        return self.col.find_one({"username":name})
    def getUsers(self):
        return self.col.find()



