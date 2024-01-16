import os
import json
import streamlit as st

from guiUtils import generateUpsertCommands, upsert, getDictionariesFolderPath
from txtai import Embeddings


def loadIndex(dictionary_file_name):
    if st.session_state.emb == None:
        st.session_state.emb = Embeddings({"path": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", "content": True})
    st.session_state.emb.load(f"indexes/{os.path.splitext(dictionary_file_name)[0]}")


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
    if emb == None:
        return "Error: there is no model connected"

    # Creazione prompt per Admin
    if st.session_state.logged_in == True:
        embedder_search_result = emb.search(f"select score, text, table_name, from txtai where similar('{user_query}') group by table_name limit 200")

        prompt = ''
        for result in embedder_search_result:
            prompt += f"Table '{result['table_name']}' have score: {result['score']};\n"

        return prompt

    # Creazione prompt per User
    else:
        embedder_search_result = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, from txtai where similar('{user_query}') and score > 0.25 group by table_name")

        dictionary_path = os.path.join(getDictionariesFolderPath(), dictionary_name)

        with open(dictionary_path, 'r') as dictionary_file:
            data = json.load(dictionary_file)

        tables_with_fields_list = []
        referencies_list = []

        for result in embedder_search_result:
            for table in data["tables"]:
                if table["name"] == result['table_name']:
                    table_with_fields = {"table_name": table["name"], "fields_list": []}

                    for column in table["columns"]:
                        field_with_description = {"field_name" : column["name"], "field_description" : column["description"]}
                        table_with_fields["fields_list"].append(field_with_description)

                        if column["references"]:
                            referencies_list.append(f"'{table['name']}.{column['name']}' references "
                                                    f"'{column['references']['table_name']}.{column['references']['field_name']}';\n")

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

        else:
            return "No relevant information was found regarding your request. \nPlease try again with a different query. \nPlease note that this application is designed to handle requests that \ncan be translated into a SQL query."