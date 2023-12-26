# versione per GUI di fileOperations.py

import os
import sys
import json
import shutil

dirPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dirPath, "..")))

database_path = os.path.join(dirPath, "..", "database")

def getFiles(file_type='.json'):
    if not os.path.exists(database_path):
        return []
    files = os.listdir(database_path)
    filtered_files = [file for file in files if file.endswith(file_type)]
    if not filtered_files:
        return []
    return filtered_files
