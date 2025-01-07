import pymongo
import logging

class OrdersDAO():
    def __init__(self,db):
        self.db =db
        self.col = db["orders"]
        logging.basicConfig(filename="database.log", encoding='utf-8',level=logging.DEBUG, format='%(asctime)s :: %(message)s')
    def newOreder(self,game,user,total):
        self.col.insert_One({
            "name":game,
            "user":user,
            "total":total})
        
    def allUserOrders(self,user):
        self.col.find({"user":user})