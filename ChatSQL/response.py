"""
This module defines classes that generate responses for the user and the technician.

The UserResponse class generates a prompt for the user based on the user's query and the sanitized input. The prompt contains information about the tables and fields in the database that are relevant to the user's query.

The TechnicianResponse class generates a debug prompt for the technician based on the user's query and the sanitized input. The prompt contains information about the similarity score of each field in the database with the user's query.
"""

import os
import json

class UserResponse:
    """
    Class that generates a prompt for the user based on the user's query and the sanitized input.
    """
    
    def __init__(self, embedder):
        self._emb = embedder

    def generate_prompt(self, user_query, sanitized_user_input, dictionary_name):
        """
        Generates a prompt for the user based on the user's query and the sanitized input.
        Args:
            - user_query (str): The user's query.
            - sanitized_user_input (str): The sanitized input.
            - dictionary_name (str): The name of the dictionary file.
        Returns:
            str: The prompt for the user."""
        embe = self._emb.get_emb()
        self._emb.load_index(dictionary_name)

        with open(os.path.join(os.path.dirname(__file__), "database", dictionary_name), 'r', encoding="utf-8") as file:
            data = json.load(file)
            embedder_search_result = embe.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, from txtai where similar('{sanitized_user_input}') and score > 0.40 group by table_name")
            tables_with_fields_list = []
            referencies_list = []

            if embedder_search_result == []:
                return "No relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that can be translated into a SQL query."
            for result in embedder_search_result:
                for table in data["tables"]:
                    if table["name"] == result['table_name']:
                        table_with_fields = {"table_name": table["name"], "fields_list": []}
                        for column in table["columns"]:
                            field_with_description = {"field_name" : column["name"], "field_description" : column["description"]}
                            table_with_fields["fields_list"].append(field_with_description)

                            if column["references"] is not None:
                                referencies_list.append(f"'{table['name']}.{column['name']}' references {column['references']['table_name']}.{column['references']['field_name']}';\n")
                        tables_with_fields_list.append(table_with_fields)

            if len(tables_with_fields_list) > 0:
                prompt = "The database contains the following tables:\n\n"
                for table in tables_with_fields_list:
                    prompt += f"table '{table['table_name']}' with fields:\n"
                    for field in table['fields_list']:
                        prompt += f"'{field['field_name']}' that contains {field['field_description']};\n"
                    prompt += "\n"
                if len(referencies_list) > 0:
                    prompt += "and the database contains the following relationships:\n"
                    for reference in referencies_list:
                        prompt += reference
                prompt += f"\nGenerate the SQL query equivalent to: {user_query}"

                embe.close()
                return prompt

class TechnicianResponse:
    def __init__(self, embedder):
        self._emb = embedder

    def generate_debug(self, user_query, sanitized_user_input, dictionary_name):
        embe = self._emb.get_emb()
        self._emb.load_index(dictionary_name)
        embedder_search_result = embe.search(f"SELECT score, text, table_name, field_name, field_description FROM txtai WHERE similar('{sanitized_user_input}') AND score > 0.01 GROUP BY table_name, field_name", limit=50)
        tables_with_fields = {}

        for result in embedder_search_result:
            table_name = result['table_name']
            field_name = result['field_name']
            field_description = result['field_description']
            score = result['score']

            if table_name not in tables_with_fields:
                tables_with_fields[table_name] = []

            tables_with_fields[table_name].append((field_name, field_description, score))

        prompt = f"Similarity score with [{user_query}] of each field in the database:\n\n"

        for table_name, fields in tables_with_fields.items():
            prompt += f"TABLE '{table_name}':\n"
            for field, description, score in fields:
                prompt += f"- FIELD: {field} {' '*(max(len(field), 14) - len(field))} | SCORE: {score:.5f} | DESCRIPTION: {description}\n"
        embe.close()
        return prompt
