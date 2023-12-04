import os
import sys
from cliAdmin import admin

def main():
    print("Welcome to the ChatSQL CLI (PLAYGROUND 🛝)")
    while True:
        print("What do you want to do?")
        print("1. Admin")
        print("2. Ask")
        print("3. Exit")
        choice = input("Your choice: ")
        if choice == "1" or choice == "admin":
            admin()
        elif choice == "2" or choice == "ask":
            pass
        elif choice == "3" or choice == "exit":
            print("Goodbye 👋")
            sys.exit()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()