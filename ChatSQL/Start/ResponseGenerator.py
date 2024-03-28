import os
import json

#from txtai import Embeddings
from embedder import *
class ResponseUser:
    def generatePrompt(self, user_query, dictionary_name):
        emb = Embedder()
        embe = emb.getEmb()
        emb.caricareIndex(dictionary_name)
        
        with open(os.path.join(os.path.dirname(__file__), "database", dictionary_name), 'r') as file:
            print("FILE:", file)

            data = json.load(file)
            embedder_search_result = embe.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, from txtai where similar('{user_query}') and score > 0.01 group by table_name")
            
            tables_with_fields_list = []
            referencies_list = []

            for result in embedder_search_result:
                for table in data["tables"]:
                    if table["name"] == result['table_name']:
                        table_with_fields = {"table_name": table["name"], "fields_list": []}

                        for column in table["columns"]:
                            field_with_description = {"field_name" : column["name"], "field_description" : column["description"]}
                            table_with_fields["fields_list"].append(field_with_description)

                            if column["references"] is not None:
                                print(column["references"])
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
                if prompt:
                    pass
                else:
                    print("prompt not existent")
                return prompt


class ResponseTechnician:
    def generateDebug(self, user_query, dictionary_name):
        emb = Embedder()
        embe = emb.getEmb()
        emb.caricareIndex(dictionary_name)
        
        with open(os.path.join(os.path.dirname(__file__), "database", dictionary_name), 'r') as file:
            print("FILE:", file)

            data = json.load(file)
            embedder_search_result = embe.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, from txtai where similar('{user_query}') and score > 0.01 group by table_name")
            
            tables_with_fields_list = []
            referencies_list = []

            prompt = '\n'
            for result in embedder_search_result:
                prompt += f"Table '{result['table_name']}' have score: {result['score']};\n"

            for result in embedder_search_result:
                for table in data["tables"]:
                    if table["name"] == result['table_name']:
                        table_with_fields = {"table_name": table["name"], "fields_list": []}

                        for column in table["columns"]:
                            field_with_description = {"field_name" : column["name"], "field_description" : column["description"]}
                            table_with_fields["fields_list"].append(field_with_description)

                            if column["references"] is not None:
                                print(column["references"])
                                referencies_list.append(f"'{table['name']}.{column['name']}' references {column['references']['table_name']}.{column['references']['field_name']}';\n")

                        tables_with_fields_list.append(table_with_fields)

            if len(tables_with_fields_list) > 0:
                prompt += "The database contains the following tables:\n\n"

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
                if prompt:
                    pass
                else:
                    print("prompt not existent")
                return prompt
