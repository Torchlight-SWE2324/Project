import os
import json
import streamlit as st

from guiUtils import generateUpsertCommands, upsert, getDictionariesFolderPath
from txtai import Embeddings

# contenuto del file va sostituito in "guiEmbedder.py" e runnato direttamente il file

def loadIndex(emb, dictionary_file_name):
    emb.load(f"indexes/{os.path.splitext(dictionary_file_name)[0]}")


def createIndex(dictionary_path):
    st.session_state.upsert_commands = generateUpsertCommands(dictionary_path)
    st.session_state.emb = upsert(st.session_state.upsert_commands)
    file_name = os.path.basename(dictionary_path)
    st.session_state.emb.save(f"indexes/{os.path.splitext(file_name)[0]}")
    st.session_state.emb.close()


def deleteIndex(dirPath, filename_to_delete_without_extension):
    indexes_folder_path = os.path.join(dirPath, "indexes")
    index_folder_to_delete_path = os.path.join(indexes_folder_path, filename_to_delete_without_extension)

    for file_to_delete in os.listdir(index_folder_to_delete_path):
        file_to_delete_path = os.path.join(index_folder_to_delete_path, file_to_delete)
        os.remove(file_to_delete_path)
    os.rmdir(index_folder_to_delete_path)


def generatePrompt(emb, user_query, dictionary_name):
    #set logged_in to true
    demo_login = False

    dictionary_path = os.path.join(getDictionariesFolderPath(), dictionary_name)

    with open(dictionary_path, 'r') as dictionary_file:
        data = json.load(dictionary_file)




    # Creazione prompt per Admin
    if demo_login:
        embedder_search_result = emb.search(f"SELECT score, text, table_name, field_name, field_description FROM txtai WHERE similar('{user_query}') AND score > 0.01 GROUP BY table_name, field_name", limit=50)

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

    # Creazione prompt per User
    else:
        embedder_search_result = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, from txtai where similar('{user_query}') and score > 0.25 group by table_name")

        prompt = ""
        
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
            return prompt

if __name__ == "__main__":

    emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})

    with open("C:/Users/Marco/Desktop/swe/progetto/ChatSQL/ChatSQL/database/auction.json", 'r') as file:
        data = json.load(file)

    commands = []

    for table in data["tables"]:
        table_name = table["name"]
        table_description = table["table-description"]

        for column in table["columns"]:
            field_name = column["name"]
            type = column["type"]
            references = column["references"]
            description = column["description"]

            # Create the emb.upsert command
            dictionary = {"table_name": table_name, "table_description": table_description, "field_name": field_name,
                          "field_type": type, "field_references": references, "field_description": description}

            commands.append(dictionary)
    

    emb.index([{"table_name": command["table_name"],
                "table_description": command["table_description"],
                "field_name": command["field_name"],
                "field_type": command["field_type"],
                "field_references": command["field_references"],
                "field_description": command["field_description"],
                "text": command["field_description"]} for command in commands])    # va cambiato il campo text dentro emb.index
    
    print(generatePrompt(emb, user_query="bid", dictionary_name="C:/Users/Marco/Desktop/swe/progetto/ChatSQL/ChatSQL/database/auction.json"))