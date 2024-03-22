from model import *
from view import *
from observer import *
#from abc import ABC, abstractmethod

class Controller(Observer):
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self.button_command_map = {}
        
    def initialize_commands(self):  
        self.button_command_map["login"] = self.login    

    def update(self):
        operazione = self._view.getOperazione()
        if operazione in self.button_command_map:
            command = self.button_command_map[operazione]
            print("Command")
            command()
            
    def login(self):
        user, psswd = self._view.getUser()
        self._model.check_login(user, psswd) 
