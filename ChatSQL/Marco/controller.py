from model import *
from view import *

class Controller:
    def __init__(self):
        self._model = Model()
        self._view = View()


    def verify_login(self):
       self._view.technician_login()
