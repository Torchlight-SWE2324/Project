import os
import sys
import re

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, '..')))

from utils import adminAuth

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
            pass
        elif re.match(r"^3$|^exit$", choice):
            confirmation = input("Are you sure you want to exit the program? (yes/no): ").lower()
            if confirmation == "yes":
                print("Exiting the program. Bye!")
                sys.exit()
            elif confirmation == "no":
                print("Returning to the main menu.")
            else:
                print("Invalid choice. Returning to the main menu.")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()