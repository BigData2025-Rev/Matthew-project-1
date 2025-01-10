from ordersDAO import OrdersDAO

class OrdersService():
    def __init__(self, dao: OrdersDAO):
        self.dao = dao
        self.games = []
    
    def addGame(self, game):
        self.games.append(game)
    def clearOrder(self):
        self.games = []
    def getTotal(self):
            total = 0
            for game in self.games:
                total += game["price"]
            return total
    def newOrder(self,userID):
        self.dao.newOreder(self.games, userID, self.getTotal())
        self.games = []
    def allUserOrders(self,userID):
        return self.dao.allUserOrders(userID)
    def allOrders(self):
        return self.dao.allOrders()
    
