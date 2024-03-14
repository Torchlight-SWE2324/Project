from Subject import Subject

class Model(Subject):
    def __init__(self):
        super().__init__()
        self._state = ""
        self._username = ""
        self._password = ""
        self.isLogged = False

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def define_login_data(self, username, password):
        self._username = username
        self._password = password

    def check_login(self, username, password):
        print("check")
        if username == "admin" and password == "admin":
            self.isLogged = True
            self.notify_observers()
            return True
        else:
            self.login_failure()
            return False
        
    def login_failure(self):
        self.isLogged = False
        self.notify_observers()

    def getIsLogedd(self):
        return self.isLogged
