# subject.py
from abc import ABC, abstractmethod

class Subject(ABC):
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    @abstractmethod
    def notify_observers(self):
        pass