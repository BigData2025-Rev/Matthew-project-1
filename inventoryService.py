from inventoryDAO import InventoryDAO
class InventoryService():
    def __init__(self, dao: InventoryDAO):
        self.dao = dao
    def newEntry(self, game, quantity,price):
        if self.dao.gameExists(game) and not self.dao.gameInInventory(game):
            self.dao.newEntry(game,quantity,price)
            return True
        else: return False
    def updateQuantity(self,name,quantity):
        self.dao.updateQuantity(name,quantity)
    def delete(self,name):
        self.dao.delete(name)
    def getInv(self):
        return self.dao.getInv()
    def getGame(self, name):
        if not self.dao.gameInInventory:
            return self.dao.getGame(name)
        else:
            return None
    def getGames(self):
        return self.dao.getGames()
