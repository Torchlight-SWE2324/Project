import os
import json
import streamlit as st

from guiUtils import generateUpsertCommands, upsert
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

def generatePromptAdmin(emb, user_query):
    if emb == None:
        return "Error: there is no model connected"

    embedder_search_result = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references from txtai where similar('{user_query}') limit 30") #da definire il limite

    prompt = ""
    for result in embedder_search_result:
        prompt = prompt+"\n"+str(result)+"\n"

    return prompt

def generatePromptUser(emb, user_query):
    if emb == None:
        return "Error: there is no model connected"

    embedder_search_result = emb.search(f"select score, text, table_name, table_description, field_name, field_type, field_references, from txtai where similar('{user_query}') limit 30") #!!! DA SOSTITUIRE "LIMIT 30"

    selected_fields_list = {}
    relationship_list = []

    ret = ""
    #?? DA METTERE " ret = "" " qua?
    for result in embedder_search_result:


        if st.session_state.logged_in == True:
            ret = "SCORE FOR DEBUGGING ONLY\n"
            ret += f"Score: {result['score']}\n"

        table_name = result['table_name']
        field_name = result['field_name']

        if table_name in selected_fields_list:
            selected_fields_list[table_name].append(field_name)
        else:
            selected_fields_list[table_name] = [field_name]

        if table_name == result['table_name'] and field_name == result['field_name'] and result['field_references']:
            references = json.loads(result['field_references'])
            relationship_list.append(f"'{table_name}.{field_name}' references '{references['table_name']}."
                            f"{references['field_name']}';\n")

    prompt = f"{ret}\nThe database contains the following tables:\n"

    for table, fields in selected_fields_list.items():
        field_str = ', '.join([f"'{field}'" for field in fields])
        prompt += f"'{table}' with fields {field_str};\n"

    if relationship_list:
        prompt += "\nand the database contains the following relationships:\n"

        for relation in relationship_list:
            prompt += relation
        prompt += f"\nGenerate the SQL query equivalent to: {user_query}"

    return prompt