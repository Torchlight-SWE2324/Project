from abc import ABC, abstractmethod
from AuthenticationHandler import AuthenticationHandler

# Interfaccia Command
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class LoginCommand(Command):
    def __init__(self, receiver: AuthenticationHandler, username: str, password: str):
        self.receiver = receiver
        self.username = username
        self.password = password

    def execute(self):
        self.receiver.login(self.username, self.password)


class LogoutCommand(Command):
    def __init__(self, receiver: AuthenticationHandler):
        self.receiver = receiver

    def execute(self):
        self.receiver.logout()


class SaveDictionaryCommand(Command): #DA FARE
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.save_dictionary()


class LoadDictionaryCommand(Command): #DA FARE
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.load_dictionary()


class DeleteDictionaryCommand(Command): #DA FARE
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.delete_dictionary()


class VisualizeSavedDictionariesCommand(Command): #DA FARE (???)
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.visualize_saved_dictionary()


class ResponseGenerationCommand(Command): #DA FARE
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.response_generation()