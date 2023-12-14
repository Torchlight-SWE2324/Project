import os
import sys
import re

from utils import adminAuth
from cliUser import user

def main():
    print("\nWelcome to the ChatSQL CLI (\033[1mPLAYGROUND\033[0m)")
    while True:
        print("\nWhat do you want to do?")
        print("1. Admin")
        print("2. Ask")
        print("3. Exit the program")
        choice = input("Your choice: ")
        if re.match(r"^1$|^admin$", choice):
            adminAuth()
        elif re.match(r"^2$|^ask$", choice):
            user()
        elif re.match(r"^3$|^exit$", choice):
            confirmation = input("Are you sure you want to exit the program? (yes/no): ").lower()
            if confirmation.lower() in ["yes", "y"]:
                print("Exiting the program. Bye!")
                sys.exit()
            elif confirmation.lower() in ["no", "n"]:
                print("Returning to the main menu.")
            else:
                print("Invalid choice. Returning to the main menu.")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()