import pymongo
from app import App

if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.get_database("boardgames")
    app = App(db)
    app.start()