import os
import sys
from jsonDecoder import json_decoder

def main():
    print("Welcome to the ChatSQL CLI")
    while True:
        inputFile = input("Enter a file to start: ")
        #if not os.path.exists(inputFile):
            #print("The file does not exist.")
        if inputFile == "exit":
            sys.exit() 
        elif inputFile == "admin":
            print("You are now logged in as admin")
        elif inputFile == "file":
            print(" this is a file")
        else:
            try:
                with open(inputFile, "r") as f:
                    contents = f.read()
                    json_data = json_decoder(contents)
            except Exception as e:
                print("Error reading or decoding JSON_old_versions file:", e)
            else:
                code = json_data
                print("Generated code:", code)
                break

if __name__ == "__main__":
    main()

# accedi
# mail: admin
# password: admin
# if data= admin => admin()
# CSV username, paswd, status