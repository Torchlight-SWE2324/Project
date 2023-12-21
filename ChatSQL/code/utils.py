import os
import sys
import csv
import time

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, '..')))

database_path = os.path.join(dirPath, "..", "database")
JSON_schema = os.path.join(dirPath, "..", "JSON", "schema.json")

def checkData(username, password):
    file_path = os.path.join(dirPath, "pswrd.csv")
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True

def leaver(section):
    confirmation = input(f"Are you sure you want to leave the {section} section? (y/n): ").lower()
    if confirmation == "yes" or confirmation == "y":
        print(f"Leaving the {section}. Bye!\n")
        return True
    elif confirmation == "no" or confirmation == "n":
        print(f"Returning to the {section} section.\n")
        return False
    else:
        print(f"Invalid choice. Returning to the {section} menu.\n")
        return False

def loading_animation(n):
    animation_chars = "|/-\\"
    start_time = time.time()

    while time.time() - start_time < n:
        for char in animation_chars:
            sys.stdout.write("\r" + "Loading " + char)
            sys.stdout.flush()
            time.sleep(0.1)

    sys.stdout.write("\r")  # Move cursor to the beginning of the line
    

if __name__ == "__main__":
    loading_animation(2)