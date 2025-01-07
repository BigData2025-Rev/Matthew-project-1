from userDAO import UserDAO
from userService import UserService

class App():
    def __init__(self, db):
        self.db = db
        self.userService = UserService(UserDAO(db))
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
        pass
    def home(self):
        pass
