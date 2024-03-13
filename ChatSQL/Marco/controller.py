from model import *
from view import *

class Controller:
    def __init__(self):
        self._model = Model()
        self._view = View()

    def change_state(self, new_state):
        self._model.set_state(new_state)
        self._view.update(self._model.get_state())

    def verify_login(self):
        #extracting the username and password from the tuple returned by the view
        usernameController, passwordController = self._view.technician_login()
        #passing the username and password to the model
        return self._model.checkLogin(usernameController, passwordController)
