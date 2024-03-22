# model.py
from subject import Subject

class BankAccount(Subject):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def withdraw(self, quantity):
        if quantity >= self.amount:
            raise ValueError("Quantity must be less than the available amount")
        self.amount -= quantity
        self.notify_observers()

    def deposit(self, quantity):
        self.amount += quantity
        self.notify_observers()

    def get_amount(self):
        return self.amount

    def notify_observers(self):
        for observer in self.observers:
            observer.update()
