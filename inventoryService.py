from inventoryDAO import InventoryDAO
class InventoryService():
    def __init__(self, dao: InventoryDAO):
        self.dao = dao
    def newEntry(self, game, quantity,price):
        if self.dao.gameExists(game) and not self.dao.gameInInventory(game):
            self.dao.newEntry(game,quantity,price)
            return True
        else: return False
    def updateGame(self,name,quantity,price):
        self.dao.updateGame(name,quantity,price)
    def delete(self,name):
        self.dao.delete(name)
    def getInv(self):
        return self.dao.getInv()
    def getGame(self, name):
        if self.dao.gameInInventory(name):
            return self.dao.getGame(name)
        else:
            return None
    def getGames(self):
        return self.dao.getGames()
    def gameExists(self, game):
        return self.dao.gameExists(game)
    def gameInInventory(self, game):
        return self.dao.gameInInventory(game)
