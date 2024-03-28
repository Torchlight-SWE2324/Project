import os
import json

#from txtai import Embeddings
from embedder import *

class ResponseUser:
    def generatePrompt(self, user_query, dictionary_name):
        emb = Embedder()
        embe = emb.getEmb()
        #get the dictionary path without using the function getDictionariesFolderPath()
        try:
            #extraxt_name = dictionary_name.split(".")[0]
            dictionary_path = os.path.join(os.path.dirname(__file__), "database", dictionary_name)

            with open(dictionary_path, 'r') as dictionary_file:
                data = json.load(dictionary_file)
            try:
                embedder_search_result = embe.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, from txtai where similar('{user_query}') and score > 0.25 group by table_name")
            except Exception as e:
                print("An error occurred in generatePrompt in ResponseGenerator:", e)
            
            tables_with_fields_list = []
            referencies_list = []

            for result in embedder_search_result:
                for table in data["tables"]:
                    if table["name"] == result['table_name']:
                        table_with_fields = {"table_name": table["name"], "fields_list": []}

                        for column in table["columns"]:
                            field_with_description = {"field_name" : column["name"], "field_description" : column["description"]}
                            table_with_fields["fields_list"].append(field_with_description)

                            if column["references"] != None:
                                print(column["references"])
                                referencies_list.append(f"'{table['name']}.{column['name']}' references {column['references']['table_name']}.{column['references']['field_name']}';\n")

                        tables_with_fields_list.append(table_with_fields)

            if len(tables_with_fields_list) > 0:
                prompt = "The data base contain the following tables:\n\n"

                for table in tables_with_fields_list:
                    prompt += f"table '{table['table_name']}' with fields:\n"

                    for field in table['fields_list']:
                        prompt += f"'{field['field_name']}' that contain {field['field_description']};\n"
                    prompt += "\n"

                if len(referencies_list) > 0:
                    prompt += "and the database contains the following relationships:\n"
                    for reference in referencies_list:
                        prompt += reference


                prompt += f"\nGenerate the SQL query equivalent to: {user_query}"
                if prompt:
                    print("PROMPT:", prompt)
                else:
                    print("prompt not existent")
            emb.generareIndex(dictionary_name)   #genera l'index (serve per test)
            emb.caricareIndex(dictionary_name)   #carica l'index dentro embedder 
            return prompt
            
        except FileNotFoundError:
            print(f"Dictionary file '{dictionary_name}' not found.")
        except Exception as e:
            print(f"An error occurred in generatePrompt2 in ResponseGenerator: {e}")

class ResponseTechnician:
    def generateDebug(self, user_query, dictionary_name):
        emb = Embedder()
        embe = emb.getEmb()
        # Creazione prompt per Admin
        try:
            embedder_search_result = embe.search(f"SELECT score, text, table_name, field_name, field_description FROM txtai WHERE similar('{user_query}') AND score > 0.01 GROUP BY table_name, field_name", limit=50)

            tables_with_fields = {}

            for result in embedder_search_result:
                table_name = result['table_name']
                field_name = result['field_name']
                field_description = result['field_description']
                score = result['score']

                if table_name not in tables_with_fields:
                    tables_with_fields[table_name] = []

                tables_with_fields[table_name].append((field_name, field_description, score ))

            prompt = "Similarity score with the user interrogation of each field in the database:\n\n"

            for table_name, fields in tables_with_fields.items():
                prompt += f"TABLE '{table_name}':\n"
                for field, description, score in fields:
                    prompt += f"- FIELD: {field} {' '*(max(len(field), 12) - len(field))} | SCORE: {score:.5f} | DESCRIPTION: {description}\n"

            return prompt
        
        except Exception as e:
            print(f"An error occurred in ResponseTechnician in ResponseGenarator: {e}")