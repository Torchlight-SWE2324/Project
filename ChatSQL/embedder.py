"""
This module defines the Embedder class, responsible for generating and loading indexes.
"""

import os
import json

from txtai import Embeddings

class Embedder:
    """
    Class that handles the generation and loading of indexes for the dictionary files.

    @para emb: the Embeddings object
    @param index_directory: the directory where the indexes are stored
    @param database_directory: the directory where the database files are stored
    @load_index_flag: flag to indicate if the index is loaded
    """
    def __init__(self):
        self._emb = None
        self._index_directory = os.path.join(os.path.dirname(__file__), "indexes")
        self._database_directory = os.path.join(os.path.dirname(__file__), "database")
        self._load_index_flag=False
    
    def generate_index(self, dictionary_file_name):
        """
        Generates an index based on the provided dictionary file.

        @param dictionary_file_name: name of the dictionary file
        @return: status message indicating success or failure
        """
        try:
            if not os.path.exists(self._index_directory):
                os.makedirs(self._index_directory)

            commands = self.generate_upsert_commands(os.path.join(self._database_directory, dictionary_file_name))
            index_name = os.path.splitext(dictionary_file_name)[0]
            index_path = os.path.join(self._index_directory, index_name)

            self.get_emb().index([{"table_name": command["table_name"],
                              "table_description": command["table_description"],
                              "field_name": command["field_name"],
                              "field_type": command["field_type"],
                              "field_references": command["field_references"],
                              "field_description": command["field_description"],
                              "text": command["field_description"]} for command in commands])

            self.get_emb().save(index_path)
            self.get_emb().close()
            return "index_created"

        except FileNotFoundError:
            return f"File '{dictionary_file_name}' or its path not found."

        except Exception as e:
            return f"An error occurred in generate_index in embedder.py: {e}"

    def generate_upsert_commands(self, dictionary_path):
        """
        Generates upsert commands from the given dictionary file.

        @param dictionary_path: path to the dictionary file
        @return: list of upsert commands
        """
        try:
            with open(dictionary_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            commands = []

            for table in data["tables"]:
                table_name = table["name"]
                table_description = table["table-description"]

                for column in table["columns"]:
                    field_name = column["name"]
                    field_type = column["type"]
                    references = column["references"]
                    description = column["description"]

                    dictionary = {"table_name": table_name,
                                "table_description": table_description,
                                "field_name": field_name,
                                "field_type": field_type, "field_references": references,
                                "field_description": description}

                    commands.append(dictionary)
            return commands

        except FileNotFoundError:
            print(f"File '{dictionary_path}' not found.")
            return []

        except json.JSONDecodeError:
            print(f"Error decoding JSON in file '{dictionary_path}'.")
            return []

        except Exception as e:
            return f"An error occurred in generate_index in embedder.py: {e}"

    def load_index(self, dictionary_file_name):
        """
        Loads an index from the specified dictionary file.

        @param dictionary_file_name: name of the dictionary file
        """
        try:
            index_name = os.path.splitext(dictionary_file_name)[0]
            index_path = os.path.join(self._index_directory, index_name)
            self.get_emb().load(index_path)
            self._load_index_flag=True

        except FileNotFoundError:
            print(f"Index file '{dictionary_file_name}' or its path not found.")
            self._load_index_flag=False

        except Exception as e:
            print(f"An error occurred in load_index in : {e}")
            self._load_index_flag=False

    def close(self):
        """Closes the current index."""
        self.get_emb().close(self._index_directory)

    def get_emb(self):
        """Gets the Embeddings object."""
        if self._emb is None:
            emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})
            self.set_emb(emb)
        return self._emb

    def set_emb(self, emb):
        """Sets the Embeddings object."""
        self._emb = emb
