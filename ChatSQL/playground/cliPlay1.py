import os
import sys
from ChatSQL.playground.cliAdmin import admin

def main():
    print("Welcome to the ChatSQL CLI (PLAYGROUND 🛝)")
    while True:
        print("1. Admin")
        print("2. User")
        print("3. Exit")
        choice = input("Your choice: ")
        if choice == "1":
            admin()
        elif choice == "2":
            pass
        elif choice == "3":
            print("Goodbye 👋")
            sys.exit()
        else:
            print("Invalid choice")
        

if __name__ == "__main__":
    main()

# accedi
# mail: admin
# password: admin
# if data= admin => admin()
# CSV username, paswd, status