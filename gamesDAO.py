import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client.get_database("boardgames")

games = db["games"]

print(games.find({"$and":[{"Year Published" : {"$exists": "true"}},{"Year Published":{"$gt":0}}]}).sort("Year Published").limit(5)[0])