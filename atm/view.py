# view.py
import sys
from subject import Subject
from observer import Observer


class CLI(Subject, Observer):
    def __init__(self, bank_account):
        super().__init__()
        self.bank_account = bank_account

    def update(self):
        self.show_account_information()

    def ask_for_next_operation(self):
        print("Select an operation: deposit or withdraw")

    def read_next_operation(self):
        current_operation = input()
        if current_operation in ["W", "D"]:
            current_quantity = input()
        self.notify_observers()

    def show_operation_not_allowed_error(self):
        print(f"The operation '{self.current_operation}' is not allowed.")

    def show_account_information(self):
        print("The current available amount is", self.bank_account.get_amount())
