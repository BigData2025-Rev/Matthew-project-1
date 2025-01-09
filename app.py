from userDAO import UserDAO
from userService import UserService
from gamesDAO import GamesDAO
from gamesService import GamesService
from inventoryDAO import InventoryDAO
from inventoryService import InventoryService
from ordersDAO import OrdersDAO
from ordersService import OrdersService
import pymongo
import sys

class App():
    def __init__(self, db):
        self.db = db
        self.userService = UserService(UserDAO(db))
        self.ordersService = OrdersService(OrdersDAO(db))
        self.inventoryService = InventoryService(InventoryDAO(db))
        self.gamesService = GamesService(GamesDAO(db))
        self.user = None

    def start(self):
        print("Welcome to the board-game store")
        while True:
            selection = input("1) login     2) sign up\n")
            if selection not in ["1","2"]:
                print("Please input 1 or 2")
                continue
            elif selection == "1":
                self.login()
                break
            else:
                self.signup()
                break

    def signup(self):
        while True:
            name = input("Enter a username:\n")
            password = input("Enter a password (must be at least 8 characters):\n")
            messsage = self.userService.newUser(name,password)
            print(messsage)
            if messsage != "User created successfully":
                continue
            else:
                self.user = self.userService.getUser(name)
                self.home()
                break
    def login(self):
        while True:
            name = input("Enter username:\n")
            password = input("Enter password:\n")
            user = self.userService.login(name,password)
            if user is None: 
                print("Incorrect username or password")

                selection = input("1) try again    2) sign up\n")
                if selection not in ["1","2"]:
                    print("Please input 1 or 2")
                    continue
                elif selection == "1":
                    continue
                else:
                    self.signup()
                    break
            else:
                self.user=user
                self.home()
                break


    def home(self):
        if not self.user["admin"]:
            while True:
                selection = input("1) New order\n2) View orders\n3) View all games\n4) Delete account\n5) Quit")
                match selection:
                    case "1":
                        self.order()
                        break
                    case "2":
                        self.viewOrders()
                        break
                    case "3":
                        self.viewGames()
                        break
                    case "4":
                        self.deleteAcc()
                        break
                    case "5":
                        sys.exit()
                    case _:
                        print("enter a number 1-5")

        else:
            while True:
                selection = input("1) New order\n2) View orders\n3) View all games\n4) Delete account\n5) Admin actions 6) Quit\n")
                match selection:
                    case "1":
                        self.order()
                        break
                    case "2":
                        self.viewOrders()
                        break
                    case "3":
                        self.viewGames()
                        break
                    case "4":
                        self.deleteAcc()
                        break
                    case "5":
                        self.admin()
                        break
                    case "6":
                        sys.exit()
                    case _:
                        print("enter a number 1-6")

    def order(self):
        def browse():
            games =self.inventoryService.getGames()
            counter = 0
            while True:
                displayedGames = []
                t="Title"
                print(f"{t:<50} Price")
                for _ in range(10):
                    game = games[counter]
                    name = game["name"]
                    price = game["price"]
                    print(f"{counter%10}) {name:<50} {price:.2f}")
                    displayedGames.append(game)
                    counter += 1
                while True:
                    selection = input("Enter a number (0-9) to add a game to your order, 'n' to continue to next page, or 'q' to quit or submit order\n")
                    if selection in [str(x) for x in range(10)]:
                        game = displayedGames[9-int(selection)]
                        self.ordersService.addGame(game)
                        print("added game to order")
                        continue
                    elif selection == "n":
                        break
                    elif selection == "q":
                        while True:
                            selection = input("submit order? y/n\n")
                            if selection == "y":
                                self.ordersService.newOrder(self.user["_id"])
                                self.ordersService.clearOrder()
                                break
                            elif selection == "n":
                                break
                            else:
                                print("Enter 'y' or 'n'")
                        return
                    else:
                        print("input not recognized")

        def search():
            while True:
                search = input("Enter name of game, or type 'q' to go back:\n")
                if search == "q":
                    break
                game = self.inventoryService.getGame(search)
                if game is None:
                    print("Game not found or unavailable")
                    continue
                else:
                    print(game["name"] + " " + str(game["price"]))
                    while True:
                        selection = input("1) add game to order\n2) search again")
                        if selection == "1":
                            self.ordersService.addGame(game)
                            while True:
                                selection = input("1) complete order\n2) search again")
                                if selection == "1":
                                    self.ordersService.newOrder(self.user["_id"])
                                    self.ordersService.clearOrder()
                                    return
                                elif selection == "2":
                                    break
                                else: 
                                    print("Enter 1 or 2")
                            break
                        elif selection == "2":
                            break
                        else:
                            print("Enter 1 or 2")

        while True:
            selection = input("1) Browse catalogue     2) Search for game by name     3) Back to home screen\n")
            if selection == "1":
                browse()
            elif selection == "2":
                search()
            elif selection == "3":
                self.home()
                break
            else:
                print("Enter 1, 2, or 3")

    def viewOrders(self):
        orders = self.ordersService.allUserOrders(self.user["_id"])
        for order in orders:
            games = order["games"]
            total = order["total"]
            print(f"games: {games}\nTotal: {total:.2f}")
    def viewGames(self):
        pass
    def deleteAcc(self):
        pass
    def admin(self):
        while True:
            selection = input("1) View inventory\n2) Edit inventory 3) Grant/remove admin access from user\n4) Return")
            match selection:
                case "1":
                    pass
                    break
                case "2":
                    pass
                    break
                case "3":
                    pass
                    break
                case "4":
                    self.home()
                    break
            

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database("boardgames")
app = App(db)
app.start()