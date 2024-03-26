from authentication import *
from view import *

class ControllerUtente:
    def __init__(self):
        self._model = None
        self._view = None

    def initialize(self, model, view):
        self._model = model
        self._view = view
            
    def login(self, username, password):
        if username != '' and password != '':
            esito = self._model.check_login(username, password)
            if esito:
                print("Login effettuato con successo")
            else:
                print("Login fallito")
        else:
            self._view.loginMancante()

    def getModel(self):
        return self._model

    def getView(self):
        return self._view
    
    def setModel(self, model):
        self._model = model

    def setView(self, view):
        self._view = view

class ControllerTecnico:
    pass

class ControllerChat:
    pass