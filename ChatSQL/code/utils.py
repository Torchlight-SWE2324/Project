import os
import sys
import csv

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, '..')))

from cliAdmin import admin

database_path = os.path.join(dirPath, "..", "database")
JSON_schema = os.path.join(dirPath, "..", "JSON", "schema.json")

def checkData(username, password):
    file_path = os.path.join(dirPath, "pswrd.csv")
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True

def adminAuth():
    username = input("Username: ")
    password = input("Password: ")
    if checkData(username, password):
        admin()
    else:
        print("username or password incorrect")