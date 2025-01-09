from gamesDAO import GamesDAO
class GamesService:
    def __init__(self, dao: GamesDAO):
        self.dao = dao
    def getAllGames(self):
        return self.dao.getAll()