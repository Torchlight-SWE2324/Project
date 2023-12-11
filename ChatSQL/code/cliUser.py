import os
import sys

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, "..")))

from fileOperations import getFiles
from embedder import emb

def user():
    os.system('clear')
    print("Welcome! Please choose a file to chat in:" + getFiles())
    #retrive the data

    #embed the data
    emb(retriveFile())

#get a file from the database
def retriveFile(filename):
    if os.path.exists(os.path.join(dirPath, "database", filename)):   #"..."
        return os.path.join(dirPath, "database", filename)
    else:
        return "Error: The file does not exist. Please check the path."

if __name__ == "__main__":
    user()
    print(retriveFile("lorem.json"))