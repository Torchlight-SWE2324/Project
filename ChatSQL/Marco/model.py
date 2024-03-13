class Model:
    def __init__(self):
        self._state = ""
        self._username = ""
        self._password = ""

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def defineLoginData(self, username, password):
        self._username = username
        self._password = password

    def checkLogin(self, username, password):
        #username = self._username
        #password = self._password
        self._username = username
        self._password = password
        if self._username == "admin" and self._password == "admin":
            return True
        else:
            return False
    
    def getLoginData(self):
        return checkLogin(self._username, self._password)
