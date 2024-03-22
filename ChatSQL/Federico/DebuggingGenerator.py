import os
import json

from txtai import Embeddings
#---Se si crea una interfaccia in comune tra DebuggingGenerator e PromptGenerator----
# from ResponseGeneratorInterface import *         
# class DebuggingGenerator(ResponseGeneratorInterface):
#------------------------------------------------------------------------------------    
class DebuggingGenerator:
    def __init__(self) -> None:
        pass



def generateResponse(emb, user_query, dictionary_path):
    # Dovremmo fare in modo nell'architettura questo non succeda
    #if emb == None:
    #    return "Error: there is no model connected"

    embedder_search_result = emb.search(f"select score, text, table_name, field_name, field_description from txtai where similar('{user_query}') group by table_name")

    with open(dictionary_path, 'r') as dictionary_file:
        data = json.load(dictionary_file)

    tables_with_fields_list = []
    prompt = ''

    for result in embedder_search_result:
            for table in data["tables"]:
                if table["name"] == result['table_name']:
                    table_with_fields = {"table_name": table["name"], "fields_list": []}

                    for column in table["columns"]:
                        field_with_description = {"field_name" : column["name"], "field_description" : column["description"], "score" : column["score"]}
                        table_with_fields["fields_list"].append(field_with_description)

                    tables_with_fields_list.append(table_with_fields)

    prompt = "Similarity score with the user interrogation of each field in the database:\n\n"

    for table in tables_with_fields_list:
        prompt += f"TABLE '{table['table_name']}':\n"

        for field in table['fields_list']:
            prompt += f"- Field '{field['field_name']}', Description '{field['field_description']}', Score '{field['score']}';\n"
        prompt += "\n"

    return prompt