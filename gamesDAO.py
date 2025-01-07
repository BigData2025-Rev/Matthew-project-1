import pymongo


class GamesDAO():
    def __init__(self, db):
        self.db = db
        self.col = db["games"]