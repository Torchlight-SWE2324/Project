import csv
import os

from abc import ABC, abstractmethod

class Authentication(ABC):
    @abstractmethod
    def check_login(self, username, password):
        pass

class AuthenticationCSV(Authentication):
    def __init__(self):
        self.username = None
        self.password = None

    def check_login(self, username, password):
        dirPath = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dirPath, "pswrd.csv")
        with open(file_path, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0] == username and row[1] == password:
                        return True
        return False
    

class AuthenticationTXT(Authentication):
    def __init__(self):
        self.username = None
        self.password = None

    def check_login(self, username, password):
        dirPath = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dirPath, "pswrd.txt")
        with open(file_path, "r") as f:
            for line in f:
                stored_username, stored_password = line.strip().split(",")
                if stored_username == username and stored_password == password:
                    return True
        return False
