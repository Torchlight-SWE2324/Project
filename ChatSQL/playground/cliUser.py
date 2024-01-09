import os
import sys

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, "..")))

from fileOperations import getFiles
from embedder import emb

def user():
    print("Welcome! Please choose a file to chat in:" + getFiles())
    
    JSON_path = os.path.abspath(os.path.join(dirPath, os.pardir, "JSON"))
    
    while True:
        # Ask for a file
        filename = input("Select a file (type 'exit' to go back): ").lower()

        # Construct the initial file path
        json_file_path = os.path.join(JSON_path, filename)

        # Check if the file exists
        if not os.path.exists(json_file_path):
            # If the file doesn't exist, try adding the .json extension
            json_file_path = os.path.join(JSON_path, f"{filename}.json")

            # Check again if the file exists
            if not os.path.exists(json_file_path):
                print(f"Error: The file '{filename}' or '{filename}.json' does not exist. Please check file name.")
                continue  # Ask for the file again

        # If a valid file is found, break out of the loop
        break
    emb(json_file_path)


if __name__ == "__main__":
    user()
