# controller.py
from observer import Observer


class Controller(Observer):
    def __init__(self, cli, bank_account):
        self.cli = cli
        self.bank_account = bank_account

    def update(self):
        operation = self.cli.get_current_operation()
        if operation == "W":
            value_to_withdraw = self.cli.get_current_quantity()
            self.bank_account.withdraw(float(value_to_withdraw))
        elif operation == "D":
            value_to_deposit = self.cli.get_current_quantity()
            self.bank_account.deposit(float(value_to_deposit))
        elif operation == "E":
            exit()