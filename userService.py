from userDAO import UserDAO
class UserService():
    def __init__(self, dao: UserDAO):
        self.dao = dao
    def newUser(self,name,password):
        if self.dao.userExists(name):
            return "User already exists"
        elif len(password) < 8:
            return "Password must be at least 8 characters"
        else:
            self.dao.newUser(name, password)
            return "User created successfully"

    def login(self,name,password):
        if self.dao.checkPW(name,password):
            return self.dao.getUser(name)
        else:
            return None
    def checkAdmin(self, name):
        return self.dao.checkAdmin(name)
    def deleteUser(self,name):
        self.dao.deleteUser(name)
    def giveAdmin(self,name):
        self.dao.giveAdmin(name)
    def removeAdmin(self,name):
        self.dao.removeAdmin(name)
    def getUser(self,name):
        return self.dao.getUser(name)