import os
import sys

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, "..")))

from fileOperations import getFiles
from embedder import emb

def user():
    os.system('clear')
    print("Welcome! Please choose a file to chat in:" + getFiles())
    
    filename = input("Select a file:")
    JSON_path = os.path.abspath(os.path.join(dirPath, os.pardir, "JSON"))
    json_file_path = os.path.join(JSON_path, filename)

    emb(json_file_path)

if __name__ == "__main__":
    user()
