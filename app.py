import pymongo
import sys
from userDAO import UserDAO
from userService import UserService
from gamesDAO import GamesDAO
from gamesService import GamesService
from inventoryDAO import InventoryDAO
from inventoryService import InventoryService
from ordersDAO import OrdersDAO
from ordersService import OrdersService


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
                input("Press enter to continue\n")
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
        print("\033c")
        if not self.user["admin"]:
            while True:
                selection = input("1) New order\n2) View orders\n3) View all games\n4) Delete account\n5) Quit\n")
                print("\033c") 
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
                selection = input("1) New order\n2) View orders\n3) View all games\n4) Delete account\n5) Admin actions\n6) Quit\n")
                print("\033c") 
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
                print("\033c")
                print(f"{'Title':<50} Price")
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
                                print("Order submitted")
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
                    price = game["price"]
                    print(game["name"] + " $" + f"{price:.2f}")
                    while True:
                        selection = input("1) add game to order\n2) search again\n")
                        if selection == "1":
                            self.ordersService.addGame(game)
                            while True:
                                selection = input("1) submit order\n2) search again\n")
                                if selection == "1":
                                    self.ordersService.newOrder(self.user["_id"])
                                    self.ordersService.clearOrder()
                                    print("Order submitted")
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
            iD = order["_id"]
            print(f"\nOrder {iD}")
            games = order["games"]
            total = order["total"]
            print("Games:")
            for game in games:
                print(game["name"])
            print(f"-------\nTotal: ${total:.2f}")
        input("Press enter to return")
        self.home()

    def viewGames(self):
        games = self.gamesService.getAllGames()
        counter = 0
        for game in games:
            if counter % 10 == 0:
                print(f"\n{'Title':<50}{'Year Released':<15}{'Players':<9}{'Minutes to Play':<17}{'Complexity(1-5)':16}{'Rating(1-10)':<12}")
                print("-"*120)
            print(f"{game['Name']:<50}{game['Year Published']:<15}{game['Min Players']:<1}-{game['Max Players']:<7}{game['Play Time']:<17}{game['Complexity Average']:<16}{game['Rating Average']:<12}")
            counter += 1
            if counter % 10 == 0:
                while True:
                    selection = input("'n' to view next page 'q' to exit\n")
                    if selection == "n":
                        break
                    elif selection == "q":
                        self.home()
                        return
                    else:
                        print("enter 'n' or 'q'")

    def deleteAcc(self):
        selection = input("Are you sure you would like to permanently delete your account? (y/n)\n")
        if selection == "y":
            self.userService.deleteUser(self.user["username"])
            print("Account deleted")
            sys.exit()
        else:self.home()

    def admin(self):
        print("\033c") 
        while True:
            selection = input("1) View inventory\n2) Edit inventory\n3) Grant/remove admin access from user\n4) View all orders\n5) Return\n")
            print("\033c") 
            match selection:
                case "1":
                    self.viewInventory()
                    break
                case "2":
                    self.editInv()
                    break
                case "3":
                    self.changeAdmin()
                    break
                case "4":
                    self.allOrders()
                    break
                case "5":
                    self.home()
                    break

    def changeAdmin(self):
        name = input("Enter username:\n")
        if self.userService.userExists(name):
            if self.userService.checkAdmin(name):
                while True:
                    selection = input(f"Remove admin access from {name}?(y/n)")
                    if selection == "y":
                        self.userService.removeAdmin(name)
                        print("access removed")
                        break
                    elif selection == "n":
                        break
                    else:
                        print("Enter y or n")
            else:
                while True:
                    selection = input(f"Give admin access to {name}?(y/n)")
                    if selection == "y":
                        self.userService.giveAdmin(name)
                        print("access granted")
                        break
                    elif selection == "n":
                        break
                    else:
                        print("Enter y or n")
        else:
            print("User not found")
        input("Press enter to return\n")
        self.admin()

    def viewInventory(self):
        games =self.inventoryService.getGames()
        print(f"{'Title':<52}{'id':<10}{'Quantity':<10}{'Price':<5}")
        for game in games:
            title = game["name"]
            iD = game["ID"]
            quantity= game["quantity"]
            price = game["price"]
            print(f"{title:<52}{iD:<10}{quantity:<10}{price:.2f}")
        input("Press enter to return\n")
        self.admin()

    def editInv(self):
        while True:
            game = input("Enter the name of game to add or change:\n")
            if self.inventoryService.gameExists(game):
                qty = int(input("Enter quantity:\n"))
                price = float(input("Enter price:\n"))
                if self.inventoryService.gameInInventory(game):
                    self.inventoryService.updateGame(game,qty,price)
                else:
                    self.inventoryService.newEntry(game,qty,price)
                break
            else: print("Invalid game entry")
        print("Update complete")
        input("Press enter to return\n")
        self.admin()
    
    def allOrders(self):
        orders = self.ordersService.allOrders()
        for order in orders:
            iD = order["_id"]
            user = order["user"]
            print(f"\nOrder {iD}")
            print(f"User ID: {user}\n")
            games = order["games"]
            total = order["total"]
            print("Games:")
            for game in games:
                print(game["name"])
            print(f"\nTotal: ${total:.2f}\n-------")
        input("Press enter to return")
        self.admin()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database("boardgames")
app = App(db)
app.start()