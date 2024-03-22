# atm.py
from view import CLI
from controller import Controller
from model import BankAccount

if __name__ == "__main__":
    bank_account = BankAccount(1000.0)
    cli = CLI(bank_account)
    controller = Controller(cli, bank_account)

    while True:
        cli.ask_for_next_operation()
        cli.read_next_operation()