import os
import sys
import csv

def checkData(username, password):
    # check if username and password are in the pswrd.csv
    # structure of the pswrd.csv
    # username, password, status
    # admin, admin, admin
    with open("pswrd.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True

def admin():
    print("ADMIN PAGE")
    # ask for username and password in input
    # check if username and password are in the pswrd.csv
    # if yes, print the status
    # if no, print "username or password incorrect"
    username = input("username: ")
    password = input("password: ")
    # check if username and password are in the pswrd.csv
    if username == "admin" and password == "admin":
        print("username and password correct")
    else:
        print("username or password incorrect")