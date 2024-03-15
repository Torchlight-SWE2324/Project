from model import *
from view import *
from observer import *
#from abc import ABC, abstractmethod

class Controller(Observer):
    def __init__(self, model, view):
        self._model = model
        self._view = view
        #self._model.attach(self)
        #self._view.attach(self)
        self.button_command_map = {}
        
    def update(self):
        user, psswd = self._view.getUser()
        self._model.check_login(user, psswd)
        

    

    """
    # get the array of users, and then pass it into the model w/ check_login
    def update(self):
        print("CONTROLLER")
        user, psswd = self._view.getUser()
        if self._model.check_login(user, psswd):
         

        #call update view
        #self._view.update()


    class UseerInputController:
    def __init__(self):
        self.button_command_map = {}

    def initialize(self):
        self.button_command_map["LoginButton"] = LoginCmd()
        self.button_command_map["LogoutButton"] = LogoutCmd()

        # Set click handlers for all buttons
        for button_label, command in self.button_command_map.items():
            button = getattr(self, button_label)
            button.on_click(self.create_click_handler(command))

    def create_click_handler(self, command):
        def click_handler():
            self.update(command)
        return click_handler

    def update(self, command):
        command.execute()
    """
