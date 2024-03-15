from subject import *
from authentication import *
class Model(Subject):
    def __init__(self):
        super().__init__()
        self._username = ""
        self._password = ""
        self.isLogged = False

    def check_login(self, username, password):
        authentication = AuthenticationCSV()
        self.isLogged = authentication.check_login(username, password)
        self.notify_observers() #notifico observer dopo aver cambiato in True

    def getIsLogedd(self):
        return self.isLogged
