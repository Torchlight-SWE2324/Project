from abc import ABC
from typing import List

from observer import *

class Subject(ABC):
    def __init__(self):
        self._observers = []
        
    def attach(self, observer):
        self._observers.append(observer)
        
    def detach(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        print("subject")
        for observer in self._observers:
            print("1")
            observer.update()
