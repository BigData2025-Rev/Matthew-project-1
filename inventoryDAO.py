import logging
class InventoryDAO():
    def __init__(self, db):
        self.db = db
        self.col = db["inventory"]
        logging.basicConfig(filename="database.log", encoding='utf-8',level=logging.INFO, format='%(asctime)s :: %(message)s')

    def newEntry(self, game, quantity, price):
        iD =  self.db["games"].find_one({"Name":game})["ID"]
        self.col.insert_one({
            "name":game,
            "ID": iD,
            "quantity":quantity,
            "price":price
        })
        logging.info("Inserted %(game)s, qty  %(quantity)s into inventory")

    def updateQuantity(self, name, quantity):
        self.col.update_one({"name":name},{"$set":{"quantity":quantity}})
        logging.info("Updated quantity of %(name)s to %(quantity)s")
    def delete(self, name):
        self.col.delete_one({"name":name})
        logging.info("%(name)s deleted from inventory")
    def getInv(self):
        return self.col.find()
    def gameExists(self,name):
        try:
            self.db["games"].find({"Name":name}).next()
            return True
        except StopIteration:
            return False
    def gameInInventory(self,name):
        try:
            self.col.find({"name":name}).next()
            return True
        except StopIteration:
            return False
    def getGame(self, name):
        return self.col.find_one({"name":name})
    def getGames(self):
        return self.col.find()
