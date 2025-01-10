import pymongo
import logging

class OrdersDAO():
    def __init__(self,db):
        self.db =db
        self.col = db["orders"]
        logging.basicConfig(filename="database.log", encoding='utf-8',level=logging.INFO, format='%(asctime)s :: %(message)s')
    def newOreder(self,games,userID,total):
        self.col.insert_one({
            "games":games,
            "user":userID,
            "total":total})
        logging.info("New order made by %s",userID)
    def allUserOrders(self,userID):
        return self.col.find({"user":userID})
    def allOrders(self):
        return self.col.find()